from django.urls import path, include
from . import views, user_login

app_name = 'users'

urlpatterns = [
    # path('accounts/', include('django.contrib.auth.urls')),
    path('forgot-password/', views.forgotPass, name='forgot_password'),
    path('index/', views.index, name='index'),
    path('doLogin',user_login.DO_LOGIN, name='doLogin'),
    path('doSignup/', user_login.DO_SIGNUP, name='doSignup'),
    path('Login/', views.Login, name='Login'),
    path('Register/', views.Register, name='Register'),
    path('Signup/', views.Signup, name='Signup'),
    
]