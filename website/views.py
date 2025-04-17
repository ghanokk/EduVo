from django.shortcuts import render

def forgotPass(request):
     return render(request, 'HTML_files/forgotPass.html')
from django.shortcuts import render

def register(request):
    return render(request, 'HTML_files/register.html')

def homePage(request):
     return render(request, 'HTML_files/homePage.html')


# Create your views here.
