from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='homePage'),
    path('ForgotPass/', views.ForgotPass, name='ForgotPass'),
    path('Jobs/', views.Jobs, name='Jobs'),
    path('History/', views.History, name='History'),
    path('Courses/', views.Courses, name='Courses'),
    path('Course_model/', views.Course_model, name='Course_model'),
    path('Login/', views.Login, name='Login'),
    path('Index/', views.Index, name='Index'),
    path('Register/', views.Register, name='Register'),

]