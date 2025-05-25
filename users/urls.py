from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('register_view/', views.register_view, name='register_view'),
    path('forgot-password/', views.forgotPass, name='forgot_password'),
    path('index/', views.index, name='index'),

    # path('signup/', views.register, name='signup'),
    # path('profile/', views.profile, name='profile'),
    # path('profile/teacher/', views.teacher_profile, name='teacher_profile'),
    # path('profile/student/', views.student_profile, name='student_profile'), 
    # path('profile/company/', views.company_profile, name='company_profile'),
]