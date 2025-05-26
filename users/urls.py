from django.urls import path, include
from . import views, user_login

app_name = 'users'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', user_login.REGISTER, name='register0'),
    path('register/', views.register1, name='register1'),
    path('register2/', views.register2, name='register2'),
    path('forgot-password/', views.forgotPass, name='forgot_password'),
    path('index/', views.index, name='index'),
    path('doLogin',user_login.DO_LOGIN, name='doLogin'),
]