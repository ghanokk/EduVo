from django.urls import path
from . import views

urlpatterns = [
    path('forgotPass/', views.forgotPass, name='forgotPass'),
    path('', views.register, name='login'),

]