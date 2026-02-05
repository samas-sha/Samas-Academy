"""
URL configuration for accounts app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('teachers/new/', views.create_teacher, name='create_teacher'),
    path('teachers/', views.teacher_list, name='teacher_list'),
]
