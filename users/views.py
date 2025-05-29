# had l'imports dyal l'views
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from courses.models import Course, Enrollment
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

# had l'function li t3aml m3a l'forgot password
def forgotPass(request):
    return render(request, 'users/forgotPass.html')

def Register(request):
    return render(request, 'users/register.html')

# had l'function li t3aml m3a l'profile dyal l'user
@login_required
def profile(request):
    user = request.user
    profile = user.profile

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
    return render(request, 'users/Signup.html')

# had l'function li t3aml m3a l'profile page

def Profile(request):
    return render(request, 'users/Profile.html')

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

# WILAYAS = [
#     (0, "Adrar"),
#     (1, "Chlef"),
#     (2, "Laghouat"),
#     (3, "Oum El Bouaghi"),
#     (4, "Batna"),
#     (5, "Béjaïa"),
#     (6, "Biskra"),
#     (7, "Béchar"),
#     (8, "Blida"),
#     (9, "Bouira"),
#     (10, "Tamanrasset"),
#     (11, "Tébessa"),
#     (12, "Tlemcen"),
#     (13, "Tiaret"),
#     (14, "Tizi Ouzou"),
#     (15, "Alger"),
#     (16, "Djelfa"),
#     (17, "Jijel"),
#     (18, "Sétif"),
#     (19, "Saïda"),
#     (20, "Skikda"),
#     (21, "Sidi Bel Abbès"),
#     (22, "Annaba"),
#     (23, "Guelma"),
#     (24, "Constantine"),
#     (25, "Médéa"),
#     (26, "Mostaganem"),
#     (27, "M’Sila"),
#     (28, "Mascara"),
#     (29, "Ouargla"),
#     (30, "Oran"),
#     (31, "El Bayadh"),
#     (32, "Illizi"),
#     (33, "Bordj Bou Arréridj"),
#     (34, "Boumerdès"),
#     (35, "El Tarf"),
#     (36, "Tindouf"),
#     (37, "Tissemsilt"),
#     (38, "El Oued"),
#     (39, "Khenchela"),
#     (40, "Souk Ahras"),
#     (41, "Tipaza"),
#     (42, "Mila"),
#     (43, "Aïn Defla"),
#     (44, "Naâma"),
#     (45, "Aïn Témouchent"),
#     (46, "Ghardaïa"),
#     (47, "Relizane"),
#     (48, "Timimoun"),
#     (49, "Bordj Badji Mokhtar"),
#     (50, "Ouled Djellal"),
#     (51, "Béni Abbès"),
#     (52, "In Salah"),
#     (53, "In Guezzam"),
#     (54, "Touggourt"),
#     (55, "Djanet"),
#     (56, "El M'Ghair"),
#     (57, "El Meniaa"),
# ]