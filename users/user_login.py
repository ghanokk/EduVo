from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from users.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy


def DO_SIGNUP(request):
  if request.method == "POST":
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
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
    user.set_password(password)#Hash
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
    
def FORGOT_PASS(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        # Simple email check (like DO_SIGNUP)
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Email doesn't exist!")
            return redirect('users:password_reset')  # Redirect back to reset page
        
        # If email exists, proceed with Django's built-in reset
        return PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            success_url=reverse_lazy('users:password_reset_done')
        )(request)
    
    # GET request: Show the reset form
    return PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    )(request)
