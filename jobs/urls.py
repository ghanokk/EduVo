from django.urls import path
from . import views

app_name = 'jobs'  # bach t3ayet l URLs b namespace

urlpatterns = [
    path('', views.job_list, name='job_list'),          # page liste ta3 l'offres
    path('<int:job_id>/', views.job_detail, name='job_detail'),  # page détails ta3 job m3a id
]
