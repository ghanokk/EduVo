from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('Forgot_Password', views.Forgot_Pass, name='Forgot_Pass'),
]