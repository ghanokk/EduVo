from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),

    path('forgotPass/', views.forgotPass, name='forgotPass'),
    path('login/', views.register, name='login'),

]