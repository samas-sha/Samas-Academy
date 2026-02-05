"""
Views for students app - CRUD, search, filter.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

from .decorators import teacher_required
from .models import Student, Department
from .forms import StudentForm


def get_teacher_decorator(view_func):
    """Apply login_required and teacher_required."""
    decorated = login_required(teacher_required(view_func))
    return decorated


@get_teacher_decorator
def student_list(request):
    """List students with search and filter."""
    students = Student.objects.select_related('department').all()

    # Search by name, roll number, or email
    search = request.GET.get('search', '').strip()
    if search:
        from django.db.models import Q
        students = students.filter(
            Q(full_name__icontains=search) | Q(roll_number__icontains=search) | Q(email__icontains=search)
        )

    # Filter by department
    dept_id = request.GET.get('department', '')
    if dept_id:
        students = students.filter(department_id=dept_id)

    # Pagination
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    departments = Department.objects.all()
    context = {
        'page_obj': page_obj,
        'departments': departments,
        'search': search,
        'selected_department': dept_id,
    }
    return render(request, 'students/student_list.html', context)


@get_teacher_decorator
def student_detail(request, pk):
    """View single student details and enrollments/grades."""
    student = get_object_or_404(Student, pk=pk)
    enrollments = student.enrollments.select_related('course', 'course__assigned_teacher').all()
    context = {'student': student, 'enrollments': enrollments}
    return render(request, 'students/student_detail.html', context)


@get_teacher_decorator
def student_create(request):
    """Add new student."""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully.')
            return redirect('student_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()

    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})


@get_teacher_decorator
def student_edit(request, pk):
    """Edit existing student."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_detail', pk=student.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {'form': form, 'student': student, 'title': 'Edit Student'})


@get_teacher_decorator
def student_delete(request, pk):
    """Delete student."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})
