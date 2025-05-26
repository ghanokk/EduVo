from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Job, Proposal

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


def job_history(request):
    # Get all jobs from the database
    jobs = Job.objects.all()
    return render(request, 'jobs/Historie.html', {jobs: jobs})

# def job_list(request):
#     # Jib kol les jobs men la base de données
#     jobs = Job.objects.all()
#     # Rendir template avec les jobs
#     return render(request, 'jobs/job_list.html', {'jobs': jobs})

def Historie(request):
    return render(request, 'jobs/Historie.html')

def job_model(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/Job-model.html', {'job': job})

def submit_proposal(request, job_id):
    if request.method == 'POST':
        try:
            job = get_object_or_404(Job, id=job_id)
            
            # Create new proposal
            proposal = Proposal.objects.create(
                job=job,
                applicant=request.user,
                full_name=request.POST.get('fullName'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                preferred_contact=request.POST.get('preferredContact'),
                cover_letter=request.POST.get('coverLetter')
            )

            # Handle file uploads if present
            if request.FILES.get('cv'):
                proposal.cv = request.FILES['cv']
            
            if request.FILES.get('certificates'):
                proposal.certificates = request.FILES['certificates']
            
            proposal.save()
            
            # Increment the applications count for the job
            job.applications_count += 1
            job.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Your application has been submitted successfully!'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

