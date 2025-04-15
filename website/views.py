from django.shortcuts import render

def ForgotPass(request):
     return render(request, 'HTML_files/ForgotPass.html')

def Register(request):
     return render(request, 'HTML_files/Register.html')

# Create your views here.
