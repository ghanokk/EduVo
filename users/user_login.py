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
    
    # Validate all inputs
    if not first_name or not last_name or not username or not email or not password:
      messages.warning(request, 'All fields are required!')
      return redirect('users:Signup')
    
    # Validate email format using regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|yahoo\.co\.uk|outlook\.com|hotmail\.com|live\.com|icloud\.com|protonmail\.com|zoho\.mail|aol\.com|edu\.dz|gov\.dz|police\.dz|armee\.dz|ens\.dz|(univ-[a-zA-Z0-9-]+)\.dz)$'
    if not re.match(email_pattern, email):
      messages.warning(request, 'Invalid email format! Please enter a valid email address.')
      return redirect('users:Signup')
    
    # Check email exists
    if User.objects.filter(email=email).exists():
      messages.warning(request, 'Email Already Exists!')
      return redirect('users:Signup')    
    
    # Check username exists
    if User.objects.filter(username=username).exists():
      messages.warning(request, 'Username Already Exists!')
      return redirect('users:Signup')
    
    # Create user only if all validations pass
    try:
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type='student'  # Assuming default user type is student
        )
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created successfully!')
        return redirect('users:Login')
    except Exception as e:
        messages.error(request, f'Error creating account: {str(e)}')
        return redirect('users:Signup')
    
  return render(request, 'users/Signup.html')

# had l'function li tjkhdm m3a login ta3 l'users
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
            return redirect('users:password_reset')
        
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
