from django.contrib import admin
from .models import Client, Document, QARecord

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file', 'client', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['file', 'client__user__username']

@admin.register(QARecord)
class QARecordAdmin(admin.ModelAdmin):
    list_display = ['question', 'document', 'asked_at']
    list_filter = ['asked_at']
    search_fields = ['question', 'document__client__user__username']


