"""
Forms for grades app - enrollment and grade assignment.
"""
from django import forms

from .models import Enrollment, Grade


class EnrollmentForm(forms.ModelForm):
    """Form to enroll a student in a course."""

    class Meta:
        model = Enrollment
        fields = ['student', 'course']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
        }


class GradeForm(forms.ModelForm):
    """Form to assign/update grade for an enrollment."""

    class Meta:
        model = Grade
        fields = ['grade_value', 'marks', 'remarks']
        widgets = {
            'grade_value': forms.Select(attrs={'class': 'form-select'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Marks'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Remarks (optional)'}),
        }
