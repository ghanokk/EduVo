from django.shortcuts import render, get_object_or_404
from courses.models import Course, Rating
from django.db.models import Q, Avg, Count
from django.apps import apps
from django.conf import settings

def forgotPass(request):
     return render(request, 'HTML_files/forgotPass.html')

def register(request):
    return render(request, 'HTML_files/register.html')

def homePage(request):
     return render(request, 'HTML_files/homePage.html')

def courses(request):
    return render(request, 'HTML_files/courses.html')


def Jobs(request):
    return render(request, 'HTML_files/Jobs.html')

def Historie(request):
    return render(request, 'HTML_files/Historie.html')

def course_model(request, course_id):
    return render(request, 'HTML_files/course-model.html')
