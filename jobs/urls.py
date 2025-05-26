from django.urls import path,include
from . import views

app_name = 'jobs'  # bach t3ayet l URLs b namespace

urlpatterns = [
    path('', views.Jobs, name='Jobs'),
    path('historie/', views.Historie, name='Historie'),
    path('job/<int:job_id>/', views.job_model, name='job-model'),
    path('job/<int:job_id>/submit-proposal/', views.submit_proposal, name='submit_proposal'),
]