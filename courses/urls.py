from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.courses, name='Courses'),
    path('<int:course_id>/', views.course_model, name='course-model'),
]