from django.shortcuts import render

def index(request):
     return render(request, 'HTML_files/index.html')

def Forgot_Pass(request):
     return render(request, 'HTML_files/forgotPass.html')
# Create your views here.
