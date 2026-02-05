"""
URL configuration for grades app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.grade_list, name='grade_list'),
    path('enroll/', views.enrollment_create, name='enrollment_create'),
    path('enroll/<int:pk>/delete/', views.enrollment_delete, name='enrollment_delete'),
    path('edit/<int:pk>/', views.grade_edit, name='grade_edit'),
    path('report/<int:student_id>/', views.grade_report, name='grade_report'),
    path('export/<int:course_id>/', views.export_students, name='export_students'),
]
