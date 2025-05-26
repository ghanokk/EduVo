from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from users.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
def DO_SIGNUP(request):
  if request.method == "POST":
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    print(first_name, last_name, username, email, password)
    #check eamil
    if User.objects.filter(email=email).exists():
      messages.warning(request, 'Email Are Already Exists !')
      return redirect('users:Signup')    
    #check username
    if User.objects.filter(username=username).exists():
      messages.warning(request, 'Username Are Already Exists !')
      return redirect('users:Signup')
    
    user = User(
      first_name = first_name,
      last_name = last_name,
      username = username,
      email = email,
    )
    user.set_password(password)
    user.save()
    return redirect('users:Login')
  return render(request, 'users/Signup.html')

def DO_LOGIN(request):
  if request.method == "POST":
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = EmailBackEnd.authenticate(request, username=email, password=password)

    if user != None:
      login(request, user)
      return redirect('website:homePage')
    else:
      messages.error(request, 'Email And Password Are Invalid')
      return redirect('users:Login')