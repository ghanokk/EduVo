from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.courses, name='Courses'),
    path('add/', views.add_course, name='add_course'),
    path('create-section/', views.create_section, name='create_section'),
    path('upload-video/', views.upload_video, name='upload_video'),
    path('upload-material/', views.upload_material, name='upload_material'),
    path('<int:course_id>/', views.course_model, name='course-model'),  # <-- Add this line
]