from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # path('forgotPass/', views.forgotPass, name='forgotPass'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgotPass, name='forgot_password'),
    # path('signup/', views.register, name='signup'),
    # path('profile/', views.profile, name='profile'),
    # path('profile/teacher/', views.teacher_profile, name='teacher_profile'),
    # path('profile/student/', views.student_profile, name='student_profile'), 
    # path('profile/company/', views.company_profile, name='company_profile'),
]