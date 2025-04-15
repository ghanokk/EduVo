from django.shortcuts import render

def forgotPass(request):
     return render(request, 'HTML_files/forgotPass.html')
from django.shortcuts import render

def register(request):
     return render(request, 'HTML_files/register.html')

# Create your views here.
