"""
Views for courses app - CRUD and teacher assignment.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import admin_required, teacher_required
from .models import Course
from .forms import CourseForm


def get_decorator(view_func):
    """Apply login_required and teacher_required."""
    return login_required(teacher_required(view_func))


@get_decorator
def course_list(request):
    """List all courses."""
    # Admin sees all; teacher sees only assigned
    if request.user.profile.is_admin():
        courses = Course.objects.select_related('department', 'assigned_teacher').all()
    else:
        courses = Course.objects.filter(assigned_teacher=request.user).select_related('department', 'assigned_teacher')
    context = {'courses': courses}
    return render(request, 'courses/course_list.html', context)


@get_decorator
def course_detail(request, pk):
    """View course details and enrolled students."""
    course = get_object_or_404(Course, pk=pk)
    # Teacher can only view their assigned courses
    if request.user.profile.is_teacher() and course.assigned_teacher != request.user:
        messages.error(request, 'Access denied.')
        return redirect('course_list')
    enrollments = course.enrollments.select_related('student', 'student__department').all()
    context = {'course': course, 'enrollments': enrollments}
    return render(request, 'courses/course_detail.html', context)


@login_required
@admin_required
def course_create(request):
    """Add new course (admin only)."""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully.')
            return redirect('course_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm()

    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Add Course'})


@login_required
@admin_required
def course_edit(request, pk):
    """Edit course (admin only)."""
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_detail', pk=course.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/course_form.html', {'form': form, 'course': course, 'title': 'Edit Course'})


@login_required
@admin_required
def course_delete(request, pk):
    """Delete course (admin only)."""
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})
