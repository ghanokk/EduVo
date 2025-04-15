from django.urls import path
from . import views

urlpatterns = [
    path('ForgotPass', views.ForgotPass, name='ForgotPass'),
    path('', views.Register, name='Login'),

]