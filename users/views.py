# had l'imports dyal l'views
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from courses.models import Course, Enrollment, Category
from jobs.models import Job, JobApplication
from skills.models import Skill, UserSkill
from users.models import User

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('homePage')
    return render(request, 'users/register.html')


# Logout view
def logout_view(request):
    auth_logout(request)
    return redirect('homePage')

def Register(request):
    return render(request, 'users/register.html')

# had l'function li t3aml m3a l'profile dyal l'user
@login_required
def profile(request):
    user = request.user
    profile = user.profile
    
    # Get user's courses
    user_courses = Course.objects.filter(creator=user).order_by('-created_at')
    
    if request.method == "POST":
        new_username = request.POST.get("new_username")
        bio = request.POST.get("bio")
        country = request.POST.get("country")
        wilaya = request.POST.get("wilaya")

        # Username validation
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, "Username already exists! Please choose another.")
            elif len(new_username) < 3:
                messages.warning(request, "Username must be at least 3 characters long.")
            else:
                user.username = new_username
                user.save()
                messages.success(request, "Username updated successfully!")

        if country:
            profile.country = country
        if bio is not None:
            profile.bio = bio
        if wilaya:
            profile.wilaya = wilaya
        profile.save()
        messages.success(request, "Profile updated successfully!")

    # nkhdmou context bach nb3atou les données l template
    context = {
        "user": user,
        "profile": profile,
        "categories": Category.objects.all(),
    }

    # nverifio l'type dyal l'user (student, teacher, company)
    if profile.is_student:
        enrollments = Enrollment.objects.filter(student=user)
        user_skills = profile.skills.all()
        job_applications = JobApplication.objects.filter(applicant=user)
        context.update({
            'stats': {
                'courses_count': enrollments.count(),
                'certificates_count': enrollments.filter(completion_status='completed').count(),
                'applications_count': job_applications.count(),
                'skills_count': user_skills.count()
            },
            'enrolled_courses': [{
                'course': enrollment.course,
            } for enrollment in enrollments[:3]],  # 3 les derniers cours
            'skills': user_skills,
            'job_applications': job_applications  # Pass all applications
        })

    if profile.is_teacher:
        taught_courses = Course.objects.filter(teacher=user)
        context.update({
            'stats': {
                'courses_count': taught_courses.count(),
                'total_students': sum(course.get_enrollment_count() for course in taught_courses),
                'reputation_score': profile.reputation_score
            },
            'taught_courses': [{
                'course': course,
                'students_count': course.get_enrollment_count(),
                'rating': course.get_average_rating(),
                'views': course.views
            } for course in taught_courses]
        })

    if profile.is_company:
        posted_jobs = Job.objects.filter(posted_by=user)
        context.update({
            'stats': {
                'jobs_count': posted_jobs.count(),
                'total_applications': sum(job.JobApplication_set.count() for job in posted_jobs)
            },
            'posted_jobs': [{
                'job': job,
                'applications_count': job.JobApplication_set.count(),
                'views': getattr(job, 'views_count', 0)
            } for job in posted_jobs]
        })

    # nreturnou l'template men les données
    return render(request, 'users/Profile.html', context)

# had l'function li t3aml m3a l'homepage
def index(request):
    return render(request, 'users/index.html')

# had l'function li t3aml m3a l'login page
def Login(request):
    return render(request, 'users/Login.html')

# had l'function li t3aml m3a l'signup page
def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # No default value needed now
        
        # Basic validation
        if not username or not email or not password:
            messages.error(request, 'All fields are required')
            return render(request, 'users/Signup.html')
            
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'users/Signup.html')
            
        # Create user with proper password hashing
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type=user_type
        )
        
        # Log the user in
        login(request, user)
        
        # Redirect to profile page
        return redirect('profile')
    
    # If GET request, just show the signup form
    return render(request, 'users/Signup.html')

# had l'function li t3aml m3a l'profile page



@login_required
def update_profile(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        new_username = request.POST.get("new_username")
        bio = request.POST.get("bio")
        country = request.POST.get("country")
        wilaya = request.POST.get("wilaya")
        errors = []

        # Username validation
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                errors.append("Username already exists! Please choose another.")
            elif len(new_username) < 3:
                errors.append("Username must be at least 3 characters long.")

        # Profile picture validation
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']
            ext = profile_picture.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                errors.append("Profile picture must be a PNG, JPG, JPEG, or GIF file.")
            elif profile_picture.size > 2 * 1024 * 1024:  # 2MB limit
                errors.append("Profile picture must be less than 2MB.")
            else:
                profile.profile_picture = profile_picture

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('users:profile')

        # If no errors, apply all changes at once
        if new_username and new_username != user.username:
            user.username = new_username
            user.save()

        if country:
            profile.country = country
        if bio is not None:
            profile.bio = bio
        if wilaya:
            profile.wilaya = wilaya
        profile.save()
        messages.success(request, "Profile updated successfully!")

    return redirect('users:profile')