"""
Forms for courses app.
"""
from django import forms
from django.contrib.auth.models import User

from students.models import Department
from .models import Course


class CourseForm(forms.ModelForm):
    """Form for add/edit course."""

    class Meta:
        model = Course
        fields = ['name', 'code', 'department', 'assigned_teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Code'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'assigned_teacher': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit teachers to users with teacher profile
        from accounts.models import UserProfile
        teacher_ids = UserProfile.objects.filter(role='teacher').values_list('user_id', flat=True)
        self.fields['assigned_teacher'].queryset = User.objects.filter(id__in=teacher_ids)
        self.fields['assigned_teacher'].required = False
