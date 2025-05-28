# had l'imports dyal l'views
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course, Enrollment
from jobs.models import Job, Proposal
from skills.models import Skill, UserSkill
from users.models import User, StudentProfile, TeacherProfile, CompanyProfile

# had l'function li t3aml m3a l'login
def login(request):
    if request.method == 'POST':
        # njibou l'username w l'password men l'form
        username = request.POST['username']
        password = request.POST['password']
        # nverifio l'authentification
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # ki l'user valid, nloginouh w ndirou redirect l'homepage
            login(request, user)
            return redirect('homePage')
    # ki ykoun GET, n'affichi l'form dyal l'login
    return render(request, 'users/register.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('homePage')

# had l'function li t3aml m3a l'forgot password
def forgotPass(request):
    return render(request, 'users/forgotPass.html')

def Register(request):
    return render(request, 'users/Register.html')

# had l'function li t3aml m3a l'profile dyal l'user
def profile(request):
    user = request.user
    # nkhdmou context bach nb3atou les données l template
    context = {
        'user': user,
    }

    # nverifio l'type dyal l'user (student, teacher, company)
    if user.user_type == 'student':
        # njibou les données dyal l'student
        student_profile = StudentProfile.objects.get(user=user)
        enrollments = Enrollment.objects.filter(student=user)
        user_skills = UserSkill.objects.filter(student_profile=student_profile)
        job_applications = Proposal.objects.filter(applicant=user)

        # nupdateou l'context men les données dyal l'student
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
            } for enrollment in enrollments[:3]],  # 3 les derniers cours
            'skills': user_skills,
            'job_applications': job_applications[:3]  # 3 les dernières applications
        })
        for course in context['enrolled_courses']:
            # print l'title dyal l'cours
            print(course['course'].title)
    elif user.user_type == 'teacher':
        # njibou les données dyal l'teacher
        teacher_profile = TeacherProfile.objects.get(user=user)
        taught_courses = Course.objects.filter(teacher=user)
        
        # nupdateou l'context men les données dyal l'teacher
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
        # njibou les données dyal l'company
        company_profile = CompanyProfile.objects.get(user=user)
        posted_jobs = Job.objects.filter(posted_by=user)
        
        # nupdateou l'context men les données dyal l'company
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
    return render(request, 'users/Signup.html')

# had l'function li t3aml m3a l'profile page

def Profile(request):
    return render(request, 'users/Profile.html')



# def Password_confirm(request):
#     return render(request, 'users/password_reset_confirm.html')

# def Password_complete(request):
#     return render(request, 'users/password_reset_complete.html')

# def Password_done(request):
#     return render(request, 'users/password_reset_done.html')

# def Password_form(request):
#     return render(request, 'users/password_reset_form.html')