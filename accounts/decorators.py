"""
Custom decorators for role-based access control.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Restrict view to admin users only."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'profile') and request.user.profile.is_admin():
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    return _wrapped_view


def teacher_required(view_func):
    """Restrict view to teacher or admin users."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'profile'):
            if request.user.profile.is_admin() or request.user.profile.is_teacher():
                return view_func(request, *args, **kwargs)
        messages.error(request, 'Access denied. Teacher or Admin privileges required.')
        return redirect('login')
    return _wrapped_view
