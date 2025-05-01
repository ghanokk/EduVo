from django.shortcuts import render

def ForgotPass(request):
     return render(request, 'HTML_files/ForgotPass.html')

def Register(request):
    return render(request, 'HTML_files/Register.html')

def HomePage(request):
     return render(request, 'HTML_files/HomePage.html')

def Course_model(request):
     return render(request, 'HTML_files/Course-model.html')

def Courses(request):
    return render(request, 'HTML_files/Courses.html')

def History(request):
     return render(request, 'HTML_files/Historie.html')

def Jobs(request) :
     return render(request, 'HTML_files/Jobs.html')

def Login(request) :
     return render(request, 'HTML_files/Login.html')

def Index(request) :
     return render(request, 'HTML_files/Index.html')




# Create your views here.

