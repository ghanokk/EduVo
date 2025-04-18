from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='homePage'),
    path('ForgotPass/', views.ForgotPass, name='ForgotPass'),
    path('Login/', views.Register, name='Login'),

]