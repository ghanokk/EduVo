from django.shortcuts import render, get_object_or_404
from .models import Job

def Jobs(request):
    # Get the latest 5 jobs for "Explore New Job Opportunities"
    new_jobs = Job.objects.filter(status='open').order_by('-created_at')[:5]
    
    # Get all open jobs for "Our Job Offers"
    all_jobs = Job.objects.filter(status='open').order_by('-created_at')
    
    # Get user's history (latest jobs they viewed)
    # Note: This is a simplified version, you might want to implement a proper history tracking system
    viewed_jobs = Job.objects.filter(status='open').order_by('-created_at')[:2]  # Showing latest 2 for now
    
    return render(request, 'jobs/Jobs.html', {
        'new_jobs': new_jobs,
        'all_jobs': all_jobs,
        'viewed_jobs': viewed_jobs
    })

def Historie(request):
    return render(request, 'jobs/Historie.html')

def job_model(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/Job-model.html', {'job': job})

