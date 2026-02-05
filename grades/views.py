"""
Views for grades app - enrollment, grade assignment, reports.
"""
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

from accounts.decorators import teacher_required
from students.models import Student
from courses.models import Course
from .models import Enrollment, Grade
from .forms import EnrollmentForm, GradeForm


def get_decorator(view_func):
    return login_required(teacher_required(view_func))


@get_decorator
def grade_list(request):
    """List enrollments/grades - filter by course or student."""
    enrollments = Enrollment.objects.select_related(
        'student', 'course', 'grade'
    ).all()

    course_id = request.GET.get('course', '')
    student_id = request.GET.get('student', '')
    if course_id:
        enrollments = enrollments.filter(course_id=course_id)
    if student_id:
        enrollments = enrollments.filter(student_id=student_id)

    context = {
        'enrollments': enrollments,
        'courses': Course.objects.all(),
        'students': Student.objects.all(),
        'selected_course': course_id,
        'selected_student': student_id,
    }
    return render(request, 'grades/grade_list.html', context)


@get_decorator
def enrollment_create(request):
    """Enroll a student in a course."""
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            if Enrollment.objects.filter(student=student, course=course).exists():
                messages.warning(request, f'{student} is already enrolled in {course}.')
            else:
                form.save()
                messages.success(request, f'{student} enrolled in {course} successfully.')
                return redirect('grade_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EnrollmentForm()

    return render(request, 'grades/enrollment_form.html', {'form': form, 'title': 'Enroll Student'})


@get_decorator
def enrollment_delete(request, pk):
    """Remove enrollment."""
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Enrollment removed successfully.')
        return redirect('grade_list')
    return render(request, 'grades/enrollment_confirm_delete.html', {'enrollment': enrollment})


@get_decorator
def grade_edit(request, pk):
    """Assign or update grade for an enrollment."""
    enrollment = get_object_or_404(Enrollment, pk=pk)
    grade, created = Grade.objects.get_or_create(enrollment=enrollment, defaults={'grade_value': None})

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, f'Grade updated for {enrollment.student} in {enrollment.course}.')
            return redirect('grade_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = GradeForm(instance=grade)

    context = {'form': form, 'enrollment': enrollment, 'title': 'Assign Grade'}
    return render(request, 'grades/grade_form.html', context)


@get_decorator
def grade_report(request, student_id):
    """View grade report for a specific student."""
    student = get_object_or_404(Student, pk=student_id)
    enrollments = Enrollment.objects.filter(student=student).select_related(
        'course', 'grade'
    )
    context = {'student': student, 'enrollments': enrollments}
    return render(request, 'grades/grade_report.html', context)


@get_decorator
def export_students(request, course_id):
    """Export enrolled students as CSV (optional feature)."""
    course = get_object_or_404(Course, pk=course_id)
    enrollments = course.enrollments.select_related('student', 'student__department').all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{course.code}_students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Roll Number', 'Full Name', 'Email', 'Department', 'Enrolled At'])

    for enr in enrollments:
        dept = enr.student.department.name if enr.student.department else '-'
        writer.writerow([
            enr.student.roll_number,
            enr.student.full_name,
            enr.student.email,
            dept,
            enr.enrolled_at.strftime('%Y-%m-%d'),
        ])

    return response
