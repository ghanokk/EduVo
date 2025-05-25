from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm
from .models import User
from django.contrib.auth import get_user_model
import uuid #generating a random, unique string

def register(request):
    x = request.POST.get('password2')
    print(x)
    return render(request, 'users/register.html')

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

def register_view(request):

    if request.method == 'POST':
        username = str(uuid.uuid4())[:30]
        email = request.POST.get('email2')
        password = request.POST.get('password2')
        x = request.POST.get('email2')
        print(x)
        
        user = User(
            username=username,  # generate unique username,
            email=email,
            password=password,
            user_type='student'
        )
        data = User(username=username, email=email )  # username is required unless you changed AUTH config
        data.set_password(password)               # hashes the password!
        data.save()
    
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')  # redirect selon my projet
#     else:
#         form = RegisterForm()
    return render(request, 'users/register.html')#, {'register_form': form, 'login_form': LoginForm()})

def login_view(request):

    # email = request.POST.get('email1')
    # password = request.POST.get('password1')
    # data = User(email=email, password=password)
    # data.save()

   if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
          form = LoginForm()
        return render(request, 'users/register.html', {'register_form': RegisterForm(), 'login_form': form})
