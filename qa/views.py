# qa/views.py

import os
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Client, Document, QARecord
from PIL import Image
from dotenv import load_dotenv

# LangChain/AI related imports
from mistralai import Mistral # Ensure you have 'mistralai' installed
from langchain_community.document_loaders import PyPDFLoader # If you were using this, ensure it's here
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS # Updated import for FAISS
from google.generativeai import GenerativeModel
import google.generativeai as genai
import uuid # For unique file names for FAISS index

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Helper functions
def convert_image_to_pdf(image_path):
    output_path = image_path.rsplit(".", 1)[0] + "_converted.pdf"
    image = Image.open(image_path).convert("RGB")
    image.save(output_path)
    return output_path

def get_pdf_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".jpg", ".jpeg", ".png"]:
        file_path = convert_image_to_pdf(file_path)
    with open(file_path, "rb") as f:
        pdf_base64 = base64.b64encode(f.read()).decode("utf-8")
    client_mistral = Mistral(api_key=MISTRAL_API_KEY) # Renamed to avoid conflict with Django's Client model
    response = client_mistral.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": f"data:application/pdf;base64,{pdf_base64}"},
        include_image_base64=False
    )
    return "\n\n".join([page.markdown for page in response.pages])

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_text(text)

def ask_ai(query, context):
    prompt = f"""
Use the following context to answer the user's question. Do calculations if needed.
Use clear paragraphs or bullet points for readability if listing information
Context:
{context}
Question: {query}
"""
    model = GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text.strip()

# Views
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
        else:
            user = User.objects.create_user(username=username, password=password)
            Client.objects.create(user=user, name=username) # Link Client to User
            messages.success(request, "Signup successful. Please login.")
            return redirect("login")
    return render(request, "qa/signup.html")

def login_view(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect("upload")
        messages.error(request, "Invalid credentials.")
    return render(request, "qa/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def home(request):
    return render(request, "qa/home.html")

@login_required
def upload(request):
    client = get_object_or_404(Client, user=request.user) # Get client linked to current user
    user_documents = Document.objects.filter(client=client).order_by('-uploaded_at') # Get documents for the current user

    if request.method == "POST":
        if "document" in request.FILES: # Handle document upload
            uploaded_file = request.FILES["document"]
            doc = Document.objects.create(client=client, file=uploaded_file)

            # Define a unique path for the FAISS index
            # Ensure 'media/faiss_indexes' exists
            faiss_index_base_dir = os.path.join("media", "faiss_indexes")
            os.makedirs(faiss_index_base_dir, exist_ok=True)

            faiss_index_dir = os.path.join(faiss_index_base_dir, str(doc.id))
            os.makedirs(faiss_index_dir, exist_ok=True)
            doc.faiss_index_path = faiss_index_dir
            doc.save() # Save the doc again to update faiss_index_path

            # Save uploaded file temporarily for processing (OCR or text extraction)
            # Use doc.file.path directly if the file is already saved by Django to a accessible path
            # Otherwise, save to a temp location.
            # Using doc.file.path is usually more direct after creation for FileField.
            temp_file_path_for_ocr = doc.file.path

            try:
                raw_text = get_pdf_text(temp_file_path_for_ocr)
                chunks = get_text_chunks(raw_text)
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
                db = FAISS.from_texts(chunks, embedding=embeddings)
                db.save_local(faiss_index_dir) # Save the FAISS index

                messages.success(request, f"Document '{uploaded_file.name}' uploaded and processed successfully!")

            except Exception as e:
                messages.error(request, f"Error processing document: {e}")
                doc.delete() # Clean up if processing fails
            finally:
                # No need to remove temp_file_path_for_ocr if it was doc.file.path
                # Django handles the FileField storage
                pass # You can remove the temporary file if you used a separate one.

            return redirect("upload") # Redirect to avoid form resubmission

        elif "query" in request.POST and "document_id" in request.POST: # Handle query for an existing document
            question = request.POST["query"]
            document_id = request.POST["document_id"]
            doc = get_object_or_404(Document, id=document_id, client=client)

            if not doc.faiss_index_path or not os.path.exists(doc.faiss_index_path):
                messages.error(request, "FAISS index not found for this document. Please re-upload or process.")
                return render(request, "qa/upload.html", {"user_documents": user_documents})

            try:
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
                db = FAISS.load_local(doc.faiss_index_path, embeddings, allow_dangerous_deserialization=True) # Load the FAISS index
                docs = db.similarity_search(question, k=3)
                context = "\n\n".join([doc.page_content for doc in docs])
                answer = ask_ai(question, context)

                # Create QARecord with auto-populated asked_at and answered_at
                QARecord.objects.create(document=doc, question=question, answer=answer)

                return render(request, "qa/upload.html", {
                    "user_documents": user_documents,
                    "answer": answer,
                    "query_asked": question,
                    "selected_document_id": document_id # Keep the selected document ID for continuity
                })
            except Exception as e:
                messages.error(request, f"Error processing query: {e}")

    return render(request, "qa/upload.html", {"user_documents": user_documents})


@login_required
def history(request):
    client = get_object_or_404(Client, user=request.user)
    # Changed from 'timestamp' to 'asked_at'
    records = QARecord.objects.filter(document__client=client).order_by("-asked_at")
    return render(request, "qa/history.html", {"records": records})

from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def delete_record(request, record_id):
    record = get_object_or_404(QARecord, id=record_id, document__client__user=request.user)
    record.delete()
    messages.success(request, "Record deleted successfully.")
    return redirect("history")