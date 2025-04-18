from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('ForgotPass', views.ForgotPass, name='ForgotPass'),
    path('', views.Register, name='Login'),
=======
    path('', views.homePage, name='homePage'),

    path('forgotPass/', views.forgotPass, name='forgotPass'),
    path('login/', views.register, name='login'),
>>>>>>> back_HomePage

]