from django.shortcuts import render, get_object_or_404
from courses.models import Course, Rating
from django.db.models import Q, Avg, Count
from django.apps import apps
from django.conf import settings
from jobs.models import Job

def forgotPass(request):
     return render(request, 'HTML_files/forgotPass.html')

def register(request):
    return render(request, 'HTML_files/register.html')

def homePage(request):
     return render(request, 'HTML_files/homePage.html')

def courses(request):
    return render(request, 'HTML_files/Courses.html')


def Jobs(request): 
    jobs = Job.objects.all()
    return render(request, 'HTML_files/Jobs.html', {'jobs': jobs})
        # return render(request, 'HTML_files/Jobs.html')

def Historie(request):
    return render(request, 'HTML_files/Historie.html')

def course_model(request, course_id):
    return render(request, 'HTML_files/course-model.html')
