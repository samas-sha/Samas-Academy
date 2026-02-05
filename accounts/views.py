"""
Views for accounts app - login, logout, dashboard, teacher management.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .decorators import admin_required, teacher_required
from .forms import LoginForm, TeacherRegistrationForm
from .models import UserProfile
from students.models import Student, Department
from courses.models import Course


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Automatically create UserProfile for superusers if missing
            if not hasattr(user, 'profile') and user.is_superuser:
                from .models import UserProfile
                UserProfile.objects.create(user=user, role='admin')
            # Check if user has a profile (admin or teacher)
            if hasattr(user, 'profile'):
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Your account does not have access to this system.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
@teacher_required
def dashboard(request):
    """Dashboard - different content for Admin vs Teacher."""
    user = request.user
    if user.profile.is_admin():
        # Admin dashboard
        context = {
            'total_students': Student.objects.count(),
            'total_courses': Course.objects.count(),
            'total_teachers': UserProfile.objects.filter(role='teacher').count(),
        }
        return render(request, 'accounts/dashboard_admin.html', context)
    else:
        # Teacher dashboard - assigned courses and enrolled students
        assigned_courses = Course.objects.filter(assigned_teacher=user)
        total_enrolled = sum(c.enrollments.count() for c in assigned_courses)
        context = {
            'assigned_courses': assigned_courses,
            'total_enrolled': total_enrolled,
        }
        return render(request, 'accounts/dashboard_teacher.html', context)


@login_required
@admin_required
def create_teacher(request):
    """Admin creates a new teacher account."""
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Teacher account created for {form.cleaned_data["username"]}.')
            return redirect('teacher_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherRegistrationForm()

    return render(request, 'accounts/teacher_form.html', {'form': form})


@login_required
@admin_required
def teacher_list(request):
    """List all teachers (admin only)."""
    teachers = UserProfile.objects.filter(role='teacher').select_related('user')
    return render(request, 'accounts/teacher_list.html', {'teachers': teachers})
