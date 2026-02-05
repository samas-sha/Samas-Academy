"""
URL configuration for courses app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('add/', views.course_create, name='course_create'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
]
