from django.urls import path
from . import views

urlpatterns = [
    path('', views.courses, name='Courses'),
    path('<int:course_id>/', views.course_model, name='course-model'),
]