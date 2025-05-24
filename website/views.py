from django.shortcuts import render, get_object_or_404
from courses.models import Course, Rating
from django.db.models import Q, Avg, Count
from django.apps import apps
from django.conf import settings
from jobs.models import Job

def register(request):
    return render(request, 'users/register.html')

def homePage(request):
    return render(request, 'website/homePage.html')

# def homePage(request):
#     # Get top courses (most viewed)
#     top_courses = Course.objects.filter(status='published').annotate(
#         avg_rating=Avg('ratings__rating_value'),
#         rating_count=Count('ratings'),
#         student_count=Count('enrollments')
#     ).order_by('-views')[:3]

#     # Get top categories with their course counts
#     top_categories = Category.objects.annotate(
#         course_count=Count('courses')
#     ).order_by('-course_count')[:4]

#     # Get latest jobs

def courses(request):
    return render(request, 'courses/Courses.html')

def Jobs(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/Jobs.html', {'jobs': jobs})

def Historie(request):
    return render(request, 'website/Historie.html')

def course_model(request, course_id):
    return render(request, 'courses/course-model.html')
