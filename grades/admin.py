"""
Django admin for grades app.
"""
from django.contrib import admin
from .models import Enrollment, Grade


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'grade_value', 'marks']
