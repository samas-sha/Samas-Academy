"""
Django admin for students app.
"""
from django.contrib import admin
from .models import Department, Student


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'roll_number', 'email', 'department']
    search_fields = ['full_name', 'roll_number', 'email']
