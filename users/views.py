# Imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from courses.models import Course, Enrollment
from jobs.models import Job, Proposal
from skills.models import Skill, UserSkill
from users.models import User, StudentProfile, TeacherProfile, CompanyProfile, WILAYA_CHOICES

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homePage')
    return render(request, 'users/register.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('homePage')

# Forgot password view
def forgotPass(request):
    return render(request, 'users/forgotPass.html')

# Register view
def Register(request):
    return render(request, 'users/Register.html')

# Profile view
def profile(request):
    user = request.user
    context = {
        'user': user,
        'WILAYA_CHOICES': WILAYA_CHOICES,
    }

    if user.user_type == 'student':
        student_profile = StudentProfile.objects.get(user=user)
        enrollments = Enrollment.objects.filter(student=user)
        user_skills = UserSkill.objects.filter(student_profile=student_profile)
        job_applications = Proposal.objects.filter(applicant=user)

        context.update({
            'profile': student_profile,
            'stats': {
                'courses_count': enrollments.count(),
                'certificates_count': enrollments.filter(completion_status='completed').count(),
                'applications_count': job_applications.count(),
                'skills_count': user_skills.count()
            },
            'enrolled_courses': [{
                'course': enrollment.course,
            } for enrollment in enrollments[:3]],
            'skills': user_skills,
            'job_applications': job_applications[:3]
        })
        for course in context['enrolled_courses']:
            print(course['course'].title)

    elif user.user_type == 'teacher':
        teacher_profile = TeacherProfile.objects.get(user=user)
        taught_courses = Course.objects.filter(teacher=user)
        
        context.update({
            'profile': teacher_profile,
            'stats': {
                'courses_count': taught_courses.count(),
                'total_students': sum(course.get_enrollment_count() for course in taught_courses),
                'reputation_score': teacher_profile.reputation_score
            },
            'taught_courses': [{
                'course': course,
                'students_count': course.get_enrollment_count(),
                'rating': course.get_average_rating(),
                'views': course.views
            } for course in taught_courses]
        })

    elif user.user_type == 'company':
        company_profile = CompanyProfile.objects.get(user=user)
        posted_jobs = Job.objects.filter(posted_by=user)
        
        context.update({
            'profile': company_profile,
            'stats': {
                'jobs_count': posted_jobs.count(),
                'total_applications': sum(job.applications.count() for job in posted_jobs)
            },
            'posted_jobs': [{
                'job': job,
                'applications_count': job.applications.count()
            } for job in posted_jobs]
        })

    return render(request, 'users/Profile.html', context)

# Homepage view
def index(request):
    return render(request, 'users/index.html')

# Login page view
def Login(request):
    return render(request, 'users/Login.html')

# Signup page view
def Signup(request):
    return render(request, 'users/Signup.html')

# Profile page view
def Profile(request):
    return render(request, 'users/Profile.html')

# Get User model
User = get_user_model()

# Update profile picture
def update_profile_picture(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            profile = request.user.get_profile()
            if request.FILES.get('profile_picture'):
                profile.profile_picture = request.FILES['profile_picture']
                profile.save()
                return JsonResponse({
                    'success': True,
                    'image_url': profile.profile_picture.url
                })
        except Exception as e:
            print(f"Error updating profile picture: {str(e)}")
    return JsonResponse({'success': False})

# Validate username
def validate_username(request):
    if request.method == 'POST':
        try:
            new_username = request.POST.get('new_username')
            current_user = request.user.username if request.user.is_authenticated else None

            exists = User.objects.filter(username=new_username).exists()
            is_current_user = (current_user == new_username)

            return JsonResponse({
                'exists': exists and not is_current_user,
                'is_valid': not exists or is_current_user,
                'message': 'Username available' if (not exists or is_current_user) else 'Username already exists'
            })
        except Exception as e:
            print(f"Error validating username: {str(e)}")
            return JsonResponse({'exists': False, 'is_valid': False, 'message': 'Error checking username'})
    return JsonResponse({'exists': False, 'is_valid': False, 'message': 'Invalid request'})

# Update profile
def update_profile(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            username = request.POST.get('username')
            wilaya = request.POST.get('wilaya')
            bio = request.POST.get('bio')
            
            if username and username != request.user.username:
                if User.objects.filter(username=username).exclude(id=request.user.id).exists():
                    return JsonResponse({'success': False, 'error': 'Username already exists'})
                request.user.username = username
                request.user.save()
            
            profile = request.user.get_profile()
            if wilaya:
                profile.wilaya = wilaya
            if bio:
                profile.bio = bio
            profile.save()
            
            return JsonResponse({
                'success': True,
                'wilaya_display': dict(WILAYA_CHOICES).get(wilaya, '')
            })
        except Exception as e:
            print(f"Error updating profile: {str(e)}")
    return JsonResponse({'success': False})

# Password_confirm view
# def Password_confirm(request):
#     return render(request, 'users/password_reset_confirm.html')

# Password_complete view
# def Password_complete(request):
#     return render(request, 'users/password_reset_complete.html')

# Password_done view
# def Password_done(request):
#     return render(request, 'users/password_reset_done.html')

# def Password_form(request):
#     return render(request, 'users/password_reset_form.html')