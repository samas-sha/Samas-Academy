"""
Courses app - Course model with teacher assignment.
"""
from django.contrib.auth.models import User
from django.db import models

from students.models import Department


class Course(models.Model):
    """Course information with assigned teacher."""
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=30, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    assigned_teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']
