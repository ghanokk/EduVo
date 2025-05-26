from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course, Enrollment
from jobs.models import Job, Proposal
from skills.models import Skill, UserSkill
from users.models import User, StudentProfile, TeacherProfile, CompanyProfile

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homePage')
    return render(request, 'users/register.html')

def forgotPass(request):
    return render(request, 'users/forgotPass.html')

def profile(request):
    user = request.user
    context = {
        'user': user,
    }

    if user.user_type == 'student':
        # Get student specific data
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
            } for enrollment in enrollments[:3]],  # Latest 3 courses
            'skills': user_skills,
            'job_applications': job_applications[:3]  # Latest 3 applications
        })
        for course in context['enrolled_courses']:
            print(course['course'].title)
    elif user.user_type == 'teacher':
        # Get teacher specific data
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
        # Get company specific data
        company_profile = CompanyProfile.objects.get(user=user)
        posted_jobs = Job.objects.filter(posted_by=user)
        
        context.update({
            'profile': company_profile,
            'stats': {
                'jobs_count': posted_jobs.count(),
                'total_applications': sum(job.proposal_set.count() for job in posted_jobs)
            },
            'posted_jobs': [{
                'job': job,
                'applications_count': job.proposal_set.count(),
                'views': job.views_count if hasattr(job, 'views_count') else 0
            } for job in posted_jobs]
        })

    return render(request, 'users/Profile.html', context)

def teacher_profile(request):
    return render(request, 'users/teacher_profile.html')

def student_profile(request):
    return render(request, 'users/student_profile.html')

def company_profile(request):
    return render(request, 'users/company_profile.html')