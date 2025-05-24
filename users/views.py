from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homePage')
    return render(request, 'users/register.html')

def forgotPass(request):
    return render(request, 'users/forgotPass.html')

def profile(request):
    return render(request, 'users/profile.html')

def teacher_profile(request):
    return render(request, 'users/teacher_profile.html')

def student_profile(request):
    return render(request, 'users/student_profile.html')

def company_profile(request):
    return render(request, 'users/company_profile.html')