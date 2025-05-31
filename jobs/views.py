from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, JobApplication, JobOffer
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F #to increment applications_count atomically
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


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
        'history_jobs': history_jobs, 
    })

def add_job(request):
    if request.method == 'POST':
        title = request.POST.get('titre', '').strip() # Remove white spaces from the input
        description = request.POST.get('description', '').strip()
        contract_type = request.POST.get('contrat', '').strip()
        expiration_date = request.POST.get('date', '').strip()
        location = request.POST.get('lieu', '').strip()
        required_skills = request.POST.get('competences', '').strip()
        industry_sector = request.POST.get('secteur', '').strip()
        education_level = request.POST.get('education', '').strip()
        job_level = request.POST.get('level', '').strip()
        company_name = request.POST.get('nom_entreprise', '').strip()
        introduction = request.POST.get('presentation', '').strip()
        contact_email = request.POST.get('email', '').strip()
        attachment = request.FILES.get('fichier')

        errors = []

        # Required fields check
        if not title:
            errors.append("Job title is required.")
        if not description:
            errors.append("Job description is required.")
        if not contract_type:
            errors.append("Contract type is required.")
        if not expiration_date:
            errors.append("Expiration date is required.")
        if not location:
            errors.append("Location is required.")
        if not required_skills:
            errors.append("Required skills are required.")
        if not industry_sector:
            errors.append("Industry sector is required.")
        if not education_level:
            errors.append("Education level is required.")
        if not job_level:
            errors.append("Job level is required.")
        if not company_name:
            errors.append("Company name is required.")
        if not introduction:
            errors.append("Introduction is required.")
        if not contact_email:
            errors.append("Contact email is required.")

        # Email validation
        if contact_email:
            try:
                validate_email(contact_email)
            except ValidationError:
                errors.append("Please enter a valid email address.")

        # File validation (optional)
        if attachment:
            allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
            ext = attachment.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                errors.append("Attachment must be a PDF, JPG, or PNG file.")
            elif attachment.size > 5 * 1024 * 1024:  # 5MB limit
                errors.append("Attachment must be less than 5MB.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'users/Profile.html')

        # If all is good, save the job offer
        JobOffer.objects.create(
            title=title,
            description=description,
            contract_type=contract_type,
            expiration_date=expiration_date,
            location=location,
            required_skills=required_skills,
            industry_sector=industry_sector,
            education_level=education_level,
            job_level=job_level,
            company_name=company_name,
            introduction=introduction,
            contact_email=contact_email,
            attachment=attachment,
            posted_by=request.user
        )
        messages.success(request, "Job offer submitted successfully!")
        return redirect('users:profile')  

    return render(request, 'users/Profile.html')