from django.contrib import admin
from .models import FileModel

class FileModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'nume', 'dimensiune']


admin.site.register(FileModel, FileModelAdmin)