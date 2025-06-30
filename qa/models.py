from django.contrib.auth.models import User
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        if self.user:
            return f"Client: {self.name} ({self.user.username})"
        return f"Client: {self.name} (No linked user)"

class Document(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    faiss_index_path = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        username = self.client.user.username if self.client.user else self.client.name
        return f"{self.file.name} | Uploaded by: {username}"

class QARecord(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    asked_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.document.client.user.username if self.document.client.user else self.document.client.name
        return f"Q by {username}: {self.question[:40]}..."
