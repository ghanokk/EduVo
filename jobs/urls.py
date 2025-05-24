from django.urls import path
from . import views

app_name = 'jobs'  # bach t3ayet l URLs b namespace

urlpatterns = [
    path('', views.jobs, name='jobs'),          # page liste ta3 l'offres
    path('<int:job_id>/', views.job_detail, name='job_detail'),  # page détails ta3 job m3a id
    path('history/', views.job_history, name='job_history'),
]
