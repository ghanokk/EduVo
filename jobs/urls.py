from django.urls import path,include
from . import views

app_name = 'job_listings'  # bach t3ayet l URLs b namespace

urlpatterns = [
    path('', views.Jobs, name='Jobs'),
    path('historie/', views.Historie, name='Historie'),
]