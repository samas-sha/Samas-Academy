"""
Students app - Student model and department/class management.
"""
from django.db import models


class Department(models.Model):
    """Department or class grouping for students."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']


class Student(models.Model):
    """Student information and enrollment details."""
    full_name = models.CharField(max_length=150)
    roll_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"

    class Meta:
        ordering = ['full_name']
