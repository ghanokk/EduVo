from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),

    path('forgotPass/', views.forgotPass, name='forgotPass'),
    path('login/', views.register, name='login'),
    path('courses/', views.Courses, name='Courses'),
    path('jobs/', views.Jobs, name='Jobs'),
    path('courses/historie/', views.Historie, name='Historie'),
    path('courses/Course_model/', views.Course_Model, name='Course_model'),





]