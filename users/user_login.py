from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from users.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
def REGISTER(request):
  if request.method == "POST":
    # first_name = request.POST.get('username')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password1')
    print(username, email, password)
    #check eamil
    if User.objects.filter(email=email).exists():
      messages.warning(request, 'Email Are Already Exists !')
      return redirect('users:register0')    
    #check username
    if User.objects.filter(username=username).exists():
      messages.warning(request, 'Username Are Already Exists !')
      return redirect('users:register0')
    
    user = User(
      username = username,
      email = email,
    )
    user.set_password(password)
    user.save()
    return redirect('users:register1')
  return render(request, 'users/register2.html')

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
      return redirect('users:register1')