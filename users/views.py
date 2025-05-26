from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import User
from django.contrib.auth import get_user_model

def forgotPass(request) :
    return render(request, 'users/forgotPass.html')

def index(request):
    return render(request, 'users/index.html')

def Login(request):
    return render(request, 'users/Login.html')

def Register(request):
    return render(request, 'users/Register.html')

def Signup(request):
    return render(request, 'users/Signup.html')