"""
Grades app - Enrollment and grade management.
"""
from django.db import models

# Import from other apps to avoid circular imports
from students.models import Student
from courses.models import Course


class Enrollment(models.Model):
    """Links students to courses (enrollment)."""
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student} - {self.course}"


class Grade(models.Model):
    """Grade assigned to a student for a course."""
    GRADE_CHOICES = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'),
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('C+', 'C+'), ('C-', 'C-'), ('D+', 'D+'), ('D-', 'D-'),
    ]

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='grade'
    )
    grade_value = models.CharField(max_length=5, choices=GRADE_CHOICES, null=True, blank=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.enrollment.student} - {self.enrollment.course}: {self.grade_value or 'N/A'}"
