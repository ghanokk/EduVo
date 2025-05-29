from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, JobApplication
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F #to increment applications_count atomically


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



def submit_application(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    field_errors = {}

    if request.method == 'POST':
        full_name = request.POST.get('fullName', '').strip()
        email = request.POST.get('email', '').strip()
        cv_file = request.FILES.get('cv')

        # Check required fields
        if not full_name:
            field_errors['fullName'] = 'Full Name is required!'
        if not email:
            field_errors['email'] = 'Email is required!'
        if not cv_file:
            field_errors['cv'] = 'CV is required!'

        # If any field error, show a general error message and re-render the form
        if field_errors:
            messages.error(request, "Your application could not be submitted. Please fill in all required fields.")
            return render(request, 'jobs/Job-model.html', {
                'job': job,
                'field_errors': field_errors,
                'form_data': request.POST,
            })

        # Optional fields
        phone = request.POST.get('phone', '').strip()
        preferred_contact = request.POST.get('preferredContact', '').strip()
        cover_letter = request.POST.get('coverLetter', '').strip()
        experience = request.POST.get('experience', '').strip()
        skills = request.POST.get('skills', '').strip()
        availability = request.POST.get('availability', '').strip()
        location = request.POST.get('location', '').strip()
        certificates = request.FILES.get('certificates')

        application = JobApplication(
            job_id=job_id,
            full_name=full_name,
            email=email,
            phone=phone,
            preferred_contact=preferred_contact,
            cv=cv_file,
            cover_letter=cover_letter,
            certificates=certificates,
            experience=experience,
            skills=skills,
            availability=availability,
            location=location,
            status='pending',  # Set initial status to pending
            applicant=request.user if request.user.is_authenticated else None
        )
        application.save()
        messages.success(request, "Application submitted successfully!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'jobs/Job-model.html', {'job': job})

def jobs_dashboard(request):
    profile = None
    skills = []
    location = ""
    history_jobs = []

    if request.user.is_authenticated:
        profile = request.user.get_profile()
        if profile:
            skills = profile.get_skills()
            location = profile.get_location()
        # Example: last 2 jobs the user applied to (customize as needed)
        history_jobs = JobApplication.objects.filter(user=request.user).order_by('-created_at')[:2]
        # Or, if you want to show recently viewed jobs, you need to implement a tracking system

    # Get the latest 5 jobs for "Explore New Job Opportunities"
    new_jobs = Job.objects.filter(status='open').order_by('-created_at')[:5]
    
    # Get all open jobs for "Our Job Offers"
    all_jobs = Job.objects.filter(status='open').order_by('-created_at')
    
    # Get user's history (latest jobs they viewed)
    # Note: This is a simplified version, you might want to implement a proper history tracking system
    viewed_jobs = Job.objects.filter(status='open').order_by('-created_at')[:2]  # Showing latest 2 for now

    return render(request, 'jobs/Jobs.html', {
        'profile': profile,
        'skills': skills,
        'location': location,
        'user': request.user,
        'new_jobs': new_jobs,
        'all_jobs': all_jobs,
        'history_jobs': history_jobs,  # Pass to template
    })