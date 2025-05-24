from django.shortcuts import render, get_object_or_404
from courses.models import Course, Rating, Category
from django.db.models import Q, Avg, Count
from django.apps import apps
from django.conf import settings
from jobs.models import Job

def register(request):
    return render(request, 'users/register.html')

def homePage(request):
    return render(request, 'website/homePage.html')


    # Get top courses (most viewed)
    top_courses = Course.objects.filter(status='published').annotate(
        avg_rating=Avg('ratings__rating_value'),
        rating_count=Count('ratings'),
        student_count=Count('enrollments')
    ).order_by('-views')[:3]

    # Get top categories with their course counts
    top_categories = Category.objects.annotate(
        course_count=Count('courses')
    ).order_by('-course_count')[:4]

    # Get latest jobs
    from jobs.models import Job
    latest_jobs = Job.objects.all().order_by('-created_at')[:6]

    # Process course data
    for course in top_courses:
        if course.image:
            course.image_url = course.image.url
        else:
            course.image_url = settings.STATIC_URL + 'assets/img/default-course.jpg'
        course.rating = range(int(course.avg_rating or 0))

    # Get statistics
    total_courses = Course.objects.filter(status='published').count()
    total_students = Course.objects.filter(status='published').aggregate(
        total=Count('enrollments', distinct=True)
    )['total'] or 0
    total_jobs = Job.objects.count()

    context = {
        'top_courses': top_courses,
        'top_categories': top_categories,
        'latest_jobs': latest_jobs,
        'stats': {
            'courses': total_courses,
            'students': total_students,
            'jobs': total_jobs
        }
    }
    
    return render(request, 'HTML_files/homePage.html', context)


#-----------------hdi ga3 homepage

def courses(request):
    return render(request, 'courses/Courses.html')

def Jobs(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/Jobs.html', {'jobs': jobs})

def Historie(request):
    return render(request, 'website/Historie.html')

def course_model(request, course_id):
    return render(request, 'courses/course-model.html')
