from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/teacher/', views.teacher_profile, name='teacher_profile'),
    path('profile/student/', views.student_profile, name='student_profile'), 
    path('profile/company/', views.company_profile, name='company_profile'),
]