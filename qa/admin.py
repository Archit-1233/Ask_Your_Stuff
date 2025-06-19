from django.contrib import admin

# Register your models here.
from .models import QARecord,Client,Document

admin.site.register(Client)
admin.site.register(QARecord)
admin.site.register(Document)

