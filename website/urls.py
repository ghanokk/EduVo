from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('forgotPass/', views.forgotPass, name='forgotPass'),  # Match the name here 
]
