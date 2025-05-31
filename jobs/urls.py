from django.urls import path,include
from . import views

app_name = 'jobs'  

urlpatterns = [
    path('', views.Jobs, name='Jobs'),
    path('job/<int:job_id>/', views.job_model, name='job-model'),
    path('job/<int:job_id>/submit-proposal/', views.submit_application, name='submit_application'),
    path('historie/', views.Historie, name='Historie'),
    path('add/', views.add_job, name='add_job'),
]

