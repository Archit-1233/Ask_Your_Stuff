# 🧠 Ask_Your_Stuff: Document & Image-based QA System

Ask_Your_Stuff is an intelligent question-answering system that allows users to upload PDFs or images, ask questions related to them, and receive contextual answers powered by advanced language models. It leverages cutting-edge technologies like LangChain, Gemini 1.5, FAISS, and Mistral OCR for seamless document understanding and retrieval.

## 🚀 Live Demo
👉 Click here to try out the app:  
**🌐 [ask-your-stuff.onrender.com](https://ask-your-stuff.onrender.com/)**  
Your intelligent PDF & image-based Q&A assistant is just a click away!

![image](https://github.com/user-attachments/assets/db6b6303-98f9-47b6-a8ea-3bb3edd7cdd6)

## 🚀 Features

- 📄 Upload PDFs or 🖼️ images (with OCR support)
- 🔍 Ask natural language questions based on your uploaded content
- 🧠 Uses Gemini 1.5 via LangChain for powerful semantic QA
- 🗂️ FAISS vector store for fast and relevant retrieval
- 🔠 Mistral OCR integration for text extraction from images
- 💾 Query and document logging using Django + SQLite
- 🌐 Streamlit frontend for an intuitive user interface

## 📸 Screenshots

###  Login Page
![image](https://github.com/user-attachments/assets/36b03837-7dab-4c96-8927-2268fac8e30f)


### Signup Page
![image](https://github.com/user-attachments/assets/d63c421d-736c-4102-8065-939994c3cfa6)


###  Upload & Ask Questions
![image](https://github.com/user-attachments/assets/7551167a-2c3d-48ce-8c6d-47d609f59b72)

### History Page
![image](https://github.com/user-attachments/assets/7b90a24d-a538-4bba-97d9-81b9a6850684)

## 🛠️ Tech Stack

| Technology      | Purpose                             |
|-----------------|-------------------------------------|
| **Streamlit**   | Frontend UI                         |
| **LangChain**   | LLM orchestration                   |
| **Gemini 1.5**  | Answer generation (LLM backend)     |
| **FAISS**       | Semantic search / vector retrieval  |
| **Mistral OCR** | Text extraction from images         |
| **Django**      | Backend + persistent logging        |
| **SQLite**      | Lightweight relational database     |

---

## 🧰 How It Works

1. **Upload**: The user uploads a PDF or image.
2. **OCR (if needed)**: Mistral API extracts text from image files.
3. **Embedding**: Document chunks are embedded using LangChain.
4. **Storage**: FAISS stores embeddings; Django logs metadata.
5. **Ask**: User poses questions; LangChain retrieves relevant context.
6. **Answer**: Gemini 1.5 responds based on extracted context.

---

## 💡 Use Cases

- Research document understanding  
- Legal or academic paper querying  
- Company report summarization  
- OCR-based invoice or form analysis  

---

## 🧪 Steps to Run the Project Locally
🔧 1. Clone the Repository
git clone https://github.com/yourusername/ask-your-stuff.git

📦 2. Create & Activate Virtual Environment (Recommended)
# Create virtual environment
python -m venv venv

# Activate it
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

📜 3. Install Required Packages
pip install -r requirements.txt

🔑 4. Configure API Keys in .env
GEMINI_API_KEY=your_google_gemini_api_key
MISTRAL_API_KEY=your_mistral_ocr_api_key

🛠️ 5. Setup Django (for Logging)
# Run migrations
python manage.py migrate

# (Optional) Create superuser to view logs in admin panel
python manage.py createsuperuser


🧠 6. Run the  App
python manage.py runserver
http://localhost:8501

## ✅ 7. Upload PDFs or Images, Ask Questions & Enjoy!
You can now:

Upload documents

Ask context-aware questions

View logged queries and files in the Django admin panel

###  🧑‍💻 Developer Info
Archit Agrawal
B.Tech CSE (AI & ML), KIET Group of Institutions
📫 agrawalarchit121@gmail.com

## 📃 License
This project is open-source and available under the MIT License.






