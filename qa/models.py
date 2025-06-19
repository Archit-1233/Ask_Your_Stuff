from django.contrib.auth.models import User
from django.db import models

class Client(models.Model):
    name=models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def self__str__(self):
        return self.name
  
class Document(models.Model):
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    faiss_index_path = models.CharField(max_length=500, null=True, blank=True) # THIS LINE IS CRUCIAL


    def __str__(self):
        return f"{self.file.name} uploaded by {self.client.name}"

class QARecord(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    
    asked_at = models.DateTimeField(auto_now_add=True)
    answered_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.question[:30]}..."




