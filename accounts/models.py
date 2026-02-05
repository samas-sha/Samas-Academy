"""
Accounts app - User roles (Admin, Teacher) and authentication.
"""
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Extends User model with role-based access (Admin or Teacher)."""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    def is_admin(self):
        return self.role == 'admin'

    def is_teacher(self):
        return self.role == 'teacher'

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
