from django.shortcuts import render 
 




def forgotPass(request):
     return render(request, 'HTML_files/forgotPass.html')



def register(request):
    return render(request, 'HTML_files/register.html')

def homePage(request):
     return render(request, 'HTML_files/homePage.html')

def Courses(request):
    return render(request, 'HTML_files/Courses.html')


def Jobs(request):
    return render(request, 'HTML_files/Jobs.html')

def Historie(request):
    return render(request, 'HTML_files/Historie.html')

def Course_Model(request):
    return render(request, 'HTML_files/Course-model.html')





# Create your views here.
