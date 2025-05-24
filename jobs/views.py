from django.shortcuts import render, get_object_or_404
from .models import Job

def jobs(request):
    return render(request, 'jobs/Jobs.html')

def job_history(request):
    return render(request, 'jobs/Historie.html')

def job_list(request):
    # Jib kol les jobs men la base de données
    jobs = Job.objects.all()
    # Rendir template avec les jobs
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    # Jib job wahed b id, ou raji3 404 si ma kaynach
    job = get_object_or_404(Job, id=job_id)
    # Rendir template détail avec job wahed
    return render(request, 'jobs/job_detail.html', {'job': job})

