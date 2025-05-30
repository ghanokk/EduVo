from django.shortcuts import render, get_object_or_404
from courses.models import Course, Rating, Category
from django.db.models import Q, Avg, Count
from django.apps import apps
from django.conf import settings
from collections import Counter



def homePage(request):
    # Get top courses (most viewed)
    top_courses = Course.objects.filter(status='published').annotate(
        avg_rating=Avg('ratings__rating_value'),
        rating_count=Count('ratings'),
        student_count=Count('enrollments')
    ).order_by('-views')[:3]

    # Get all categories used in courses
    course_categories = Course.objects.values_list('category', flat=True)
    category_counts = Counter(course_categories)

    # Get top categories by count
    top_categories = sorted(
        [{'name': name, 'count': count} for name, count in category_counts.items()],
        key=lambda x: -x['count']
    )[:4]

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
