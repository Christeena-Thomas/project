# admin.py
from django.contrib import admin
from .models import ExcelFile, UserRegistration, Event
import os

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']

@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'department']

@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'uploaded_at']

    def file_name(self, obj):
        return os.path.basename(obj.file.name)
    file_name.short_description = 'File Name'

    def upload_excel(self, request, queryset):
        for obj in queryset:
            # Access the uploaded file
            uploaded_file = obj.file  # Changed from obj.file_field to obj.file

            # Process and save the uploaded file
            # For example, save the file to the filesystem
            with open(uploaded_file.path, 'rb') as file:
                # Process the file (e.g., read its contents, parse it, etc.)
                # Example: Print the contents of the file
                file_contents = file.read()
                print(file_contents)

            # You can also save the file to the database if needed
            # For example: obj.save()

    upload_excel.short_description = "Upload Excel File"