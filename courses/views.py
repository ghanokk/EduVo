import os
from django.shortcuts import render, get_object_or_404
from courses.models import Course, Rating,Lesson,WhatYouLearn
from django.db.models import Q, Avg, Count
from django.apps import apps
from django.conf import settings

# Q: nstakhdmoha bach ndir des filtres flexibles b AND, OR, ou NOT
# Avg: tcalculi moyenne d'une colonne (hna rating_value)
# Count: tcalculi nombre d'objets (ex: nombre d'étudiants ou de ratings)

def courses(request):
    # njiبو les paramètres de filtre men URL (GET)
    search_query = request.GET.get('search', '').strip()
    categories = request.GET.getlist('category')
    rating = request.GET.get('rating', '')
    price_type = request.GET.get('price_type', '')
    level = request.GET.get('level', '')

    # ndirou requête principale: ghir les cours publiés
    # w nzidou avg_rating, rating_count, student_count b des annotations
    courses = Course.objects.filter(status='published').annotate(
        avg_rating=Avg('ratings__rating_value'),
        rating_count=Count('ratings'),
        student_count=Count('enrollments')
    )

    # Search only by course title and category name
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # ki ykounu catégories mkhtarin
    if categories:
        # Get category objects from IDs
        category_ids = [int(cat) for cat in categories if cat.isdigit()]
        if category_ids:
            courses = courses.filter(category_id__in=category_ids)

    # Filter by rating if selected
    if rating:
        try:
            rating = float(rating)
            if rating == 0:
                # Show all courses
                pass
            elif rating == 1:
                # Show courses with rating 0.1-1.0
                courses = courses.filter(avg_rating__gte=0.1, avg_rating__lte=1.0)
            elif rating == 2:
                # Show courses with rating 1.1-2.0
                courses = courses.filter(avg_rating__gt=1.0, avg_rating__lte=2.0)
            elif rating == 3:
                # Show courses with rating 2.1-3.0
                courses = courses.filter(avg_rating__gt=2.0, avg_rating__lte=3.0)
            elif rating == 4:
                # Show courses with rating 3.1-4.0
                courses = courses.filter(avg_rating__gt=3.0, avg_rating__lte=4.0)
            elif rating == 5:
                # Show courses with rating 4.1-5.0
                courses = courses.filter(avg_rating__gt=4.0, avg_rating__lte=5.0)
        except ValueError:
            # Invalid rating value, ignore it
            pass

    # filtrage 3la les prix: gratuit ou payant
    if price_type == 'paid':
        courses = courses.filter(price__gt=0)
    elif price_type == 'free':
        courses = courses.filter(price=0)

    # filtre selon le niveau (level)
    if level:
        courses = courses.filter(level=level)

    # njibou toutes les catégories distinctes (pour le menu dropdown)
    all_categories = Course.objects.values_list('category_id', 'category__name').distinct()

    # njibou top 5 des cours les plus vus
    top_courses = Course.objects.filter(status='published').order_by('-views')[:5]

    # nkhdmou info zyada 3la chaque cours
    for course in courses:
        # n7awlou avg_rating l range bach n'affichi les étoiles
        course.rating = range(int(course.avg_rating or 0))
        # total d'heures dyal contenu
        course.total_hours = course.get_total_duration()
        # nombre de leçons
        course.lectures = course.get_total_lessons()
        # traitement d'image: si kayna, ykhdemha, sinon default
        if course.image:
            course.image_url = course.image.url
        else:
            course.image_url = settings.STATIC_URL + 'assets/img/default-course.jpg'

    # meme traitement pour top_courses
    for course in top_courses:
        if course.image:
            course.image_url = course.image.url
        else:
            course.image_url = settings.STATIC_URL + 'assets/img/default-course.jpg'

    # kol data ndakhlouha f context bach n'affichiha f template
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

    return render(request, 'courses.html', context)

# function li taffichi wahad lcourse selon l'id
def course_model(request, course_id):
    # njibou cours wla ndirou erreur 404 si makaynach
    course = get_object_or_404(Course, id=course_id, status='published')

    # njibou les ratings dyal had lcourse, ordonnés par date de création
    ratings = course.ratings.all().order_by('-created_at')

    # njibou la moyenne des ratings
    avg_rating = course.ratings.aggregate(Avg('rating_value'))['rating_value__avg'] or 0

    # nzidou 1 f views bach naffichi nombre de vues
    course.views += 1
    course.save()

    # traitement d'image: ydir image luser sinon ydir image par défaut
    if course.image:
        course.image_url = course.image.url
    else:
        course.image_url = settings.STATIC_URL + 'assets/img/default-course.jpg'

    # n7awlou avg_rating l étoiles (range)
    course.rating = range(int(avg_rating))

    # Debug information
    print(f"Course ID: {course.id}")
    print(f"Course Title: {course.title}")
    print(f"Sections count: {course.sections.count()}")
    print(f"Lessons count: {Lesson.objects.filter(section__course=course).count()}")

    # nkhdmou context bach nb3atou les données l template
    context = {
        'course': course,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'rating_count': ratings.count(),
        'student_count': course.enrollments.count(),
        'sections': course.sections.prefetch_related('lessons').all(),
        'lessons': Lesson.objects.filter(section__course=course).order_by('section__order', 'order'),
        'lessons_count': course.get_total_lessons(),
        'total_hours': course.get_total_duration(),
        'teacher': course.teacher,
        'teacher_title': getattr(course.teacher, 'profile', {}).get('title', ''),
        'what_you_learn': course.what_you_learn.all(),
    }

    return render(request, 'Course-model.html', context)
