from django.shortcuts import render

def ForgotPass(request):
     return render(request, 'HTML_files/ForgotPass.html')

<<<<<<< HEAD
def Register(request):
     return render(request, 'HTML_files/Register.html')
=======
def register(request):
    return render(request, 'HTML_files/register.html')

def homePage(request):
     return render(request, 'HTML_files/homePage.html')

>>>>>>> back_HomePage

# Create your views here.
