from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views,user_login
from .user_login import DO_LOGIN, DO_SIGNUP

app_name = 'users'

urlpatterns = [
    # path('accounts/', include('django.contrib.auth.urls')),
    path('index/', views.index, name='index'),
    path('Register/', views.Register, name='Register'),
    path('Login/', views.Login, name='Login'),
    path('Signup/', views.Signup, name='Signup'),
    path('doLogin',user_login.DO_LOGIN, name='doLogin'),
    path('doSignup/', user_login.DO_SIGNUP, name='doSignup'),
    path('profile', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),  
    path('forgot_password/', user_login.FORGOT_PASS, name='forgot_password'),  

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             success_url=reverse_lazy('users:password_reset_done') 
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url=reverse_lazy('users:password_reset_complete')  
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
         
    path('update-profile/', views.update_profile, name='update_profile'),
]