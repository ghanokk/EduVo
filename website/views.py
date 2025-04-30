from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages



def forgotPass(request):
     return render(request, 'HTML_files/forgotPass.html')



def register(request):
    return render(request, 'HTML_files/register.html')

def homePage(request):
     return render(request, 'HTML_files/homePage.html')




# Create your views here.
