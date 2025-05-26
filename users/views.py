from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import User
from django.contrib.auth import get_user_model

def register0(request):
    return render(request, 'users/register0.html')

def register1(request):
    return render(request, 'users/register.html')

def register2(request):
    return render(request, 'users/register2.html')

def forgotPass(request) :
    return render(request, 'users/forgotPass.html')

def index(request):
    return render(request, 'users/index.html')
    
def profile(request):
    return render(request, 'users/profile.html')

def teacher_profile(request):
    return render(request, 'users/teacher_profile.html')

def student_profile(request):
    return render(request, 'users/student_profile.html')

def company_profile(request):
    return render(request, 'users/company_profile.html')


