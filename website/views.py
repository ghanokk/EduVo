from django.shortcuts import render

def ForgotPass(request):
     return render(request, 'HTML_files/ForgotPass.html')

def Register(request):
    return render(request, 'HTML_files/Register.html')

def HomePage(request):
     return render(request, 'HTML_files/HomePage.html')


# Create your views here.
