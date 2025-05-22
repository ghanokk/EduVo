from django.shortcuts import render, get_object_or_404
from courses.models import Course, Rating
from django.db.models import Q, Avg, Count
from django.apps import apps
from django.conf import settings
# Q permet de faire des requêtes complexes avec des conditions OU (OR), ET (AND), ou des conditions négatives (NOT), dans Django ORM.
#Avg calcul the 
def courses(request):
    # Get filter parameters
    search_query = request.GET.get('search', '')
    categories = request.GET.getlist('category')
    rating = request.GET.get('rating', '')
    price_type = request.GET.get('price_type', '')
    level = request.GET.get('level', '')

    # Base queryset with annotations for ratings
    courses = Course.objects.filter(status='published').annotate(
        avg_rating=Avg('ratings__rating_value'),
        rating_count=Count('ratings'),
        student_count=Count('enrollments')
    )

    # Apply filters
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    if categories:
        courses = courses.filter(category__in=categories)

    if rating:
        rating = int(rating)
        courses = courses.filter(avg_rating__gte=rating)

    if price_type == 'paid':
        courses = courses.filter(price__gt=0)
    elif price_type == 'free':
        courses = courses.filter(price=0)

    if level:
        courses = courses.filter(level=level)

    # Get distinct categories for dropdown
    all_categories = Course.objects.values_list('category', flat=True).distinct()

    # Get top courses (most viewed)
    top_courses = Course.objects.filter(status='published').order_by('-views')[:5]

    # Add additional course data
    for course in courses:
        # Convert average rating to stars
        course.rating = range(int(course.avg_rating or 0))
        course.total_hours = course.get_total_duration()
        course.lectures = course.get_total_lessons()
        # Handle image URL properly
        if course.image:
            course.image_url = course.image.url
        else:
            course.image_url = settings.STATIC_URL + 'assets/img/default-course.jpg'

    # Add data for top courses
    for course in top_courses:
        if course.image:
            course.image_url = course.image.url
        else:
            course.image_url = settings.STATIC_URL + 'assets/img/default-course.jpg'

    context = {
        'courses': courses,
        'top_courses': top_courses,
        'search_query': search_query,
        'categories': all_categories,
        'selected_categories': categories,
        'selected_rating': rating,
        'selected_price_type': price_type,
        'selected_level': level,
        'level_choices': Course.LEVEL_CHOICES,
    }
    return render(request, 'HTML_files/courses.html', context)

def course_model(request, course_id):
    course = get_object_or_404(Course, id=course_id, status='published')
    
    # Get course ratings
    ratings = course.ratings.all().order_by('-created_at')
    
    # Calculate average rating
    avg_rating = course.ratings.aggregate(Avg('rating_value'))['rating_value__avg'] or 0
    
    # Increment views when someone visits the page
    course.views += 1
    course.save()
    
    # Handle image URL properly
    if course.image:
        course.image_url = course.image.url
    else:
        course.image_url = settings.STATIC_URL + 'assets/img/default-course.jpg'
    
    # Add rating stars for display
    course.rating = range(int(avg_rating))
    
    context = {
        'course': course,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'rating_count': ratings.count(),
        'student_count': course.enrollments.count(),
    }
    return render(request, 'courses/course-model.html', context)