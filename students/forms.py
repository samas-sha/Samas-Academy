"""
Forms for students app.
"""
from django import forms
from .models import Student, Department


class StudentForm(forms.ModelForm):
    """Form for add/edit student."""

    class Meta:
        model = Student
        fields = ['full_name', 'roll_number', 'email', 'phone', 'date_of_birth', 'department']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Roll Number / Student ID'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
        }
