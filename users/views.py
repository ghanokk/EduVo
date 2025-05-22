from django.shortcuts import render

def register(request):
    return render(request, 'HTML_files/register.html')

def profile(request):
    return render(request, 'users/profile.html')

def teacher_profile(request):
    return render(request, 'users/teacher_profile.html')

def student_profile(request):
    return render(request, 'users/student_profile.html')

def company_profile(request):
    return render(request, 'users/company_profile.html')