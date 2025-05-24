from django.urls import path
from . import views

app_name = 'user_accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('forgotPass/', views.forgotPass, name='forgotPass'),

    path('profile/teacher/', views.teacher_profile, name='teacher_profile'),
    path('profile/student/', views.student_profile, name='student_profile'), 
    path('profile/company/', views.company_profile, name='company_profile'),
]