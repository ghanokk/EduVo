from django.shortcuts import render, get_object_or_404
from .models import Job

def Jobs(request):
    return render(request, 'jobs/Jobs.html')

def Historie(request):
    return render(request, 'jobs/Historie.html')

def Jobs(request):
    return render(request, 'jobs/Jobs.html')