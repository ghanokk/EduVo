from django.shortcuts import render

def ForgotPass(request):
     return render(request, 'HTML_files/ForgotPass.html')

def register(request):
    return render(request, 'HTML_files/register.html')

def homePage(request):
     return render(request, 'HTML_files/homePage.html')


# Create your views here.
