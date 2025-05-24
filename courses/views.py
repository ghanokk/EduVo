from django.shortcuts import render, get_object_or_404
from courses.models import Course, Rating
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

    # ki ykoun search: nfiltriw 3la titre, description, ou catégorie
    if search_query:
        # Split search terms and create conditions
        search_terms = search_query.lower().split()
        
        # Create conditions that match similar words
        title_conditions = []
        desc_conditions = []
        category_conditions = []
        
        for term in search_terms:
            # Create dynamic variations based on common confusions
            variations = [
                term,  # original term
                # Vowel variations
                term.replace('a', 'e'), term.replace('e', 'a'),
                term.replace('i', 'y'), term.replace('y', 'i'),
                term.replace('o', 'u'), term.replace('u', 'o'),
                # Consonant variations
                term.replace('r', 'l'), term.replace('l', 'r'),
                term.replace('w', 'v'), term.replace('v', 'w'),
                term.replace('c', 'k'), term.replace('k', 'c'),
                term.replace('s', 'z'), term.replace('z', 's'),
                # Double letter variations
                term.replace('ss', 's'), term.replace('ee', 'e'),
                term.replace('ll', 'l'), term.replace('rr', 'r'),
                # Common misspellings
                term.replace('th', 't'), term.replace('ph', 'f'),
                term.replace('ch', 'c'), term.replace('sh', 's'),
            ]
            
            # Remove duplicates
            variations = list(set(variations))
            
            # Add all variations to conditions
            for variation in variations:
                title_conditions.append(Q(title__icontains=variation))
                desc_conditions.append(Q(description__icontains=variation))
                category_conditions.append(Q(category__name__icontains=variation))
        
        # Combine conditions using OR within each field
        title_q = Q(title_conditions[0]) if title_conditions else Q()
        desc_q = Q(desc_conditions[0]) if desc_conditions else Q()
        category_q = Q(category_conditions[0]) if category_conditions else Q()
        
        for cond in title_conditions[1:]:
            title_q |= cond
        for cond in desc_conditions[1:]:
            desc_q |= cond
        for cond in category_conditions[1:]:
            category_q |= cond
        
        # Combine all fields using OR
        courses = courses.filter(title_q | desc_q | category_q)
    
    # ki ykounu catégories mkhtarin
    if categories:
        # Get category objects from IDs
        category_ids = [int(cat) for cat in categories if cat.isdigit()]
        if category_ids:
            courses = courses.filter(category_id__in=category_ids)

    # ki ykoun rating m3ayin (min): ndirou filtre b avg_rating >= rating
    if rating:
        rating = int(rating)
        courses = courses.filter(avg_rating__gte=rating)

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

    return render(request, 'Courses.html', context)

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

    # nkhdmou context bach nb3atou les données l template
    context = {
        'course': course,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'rating_count': ratings.count(),
        'student_count': course.enrollments.count(),
        'sections': course.sections.all(),
        'lessons_count': course.get_total_lessons(),
        'total_hours': course.get_total_duration(),
        'teacher': course.teacher,
        'teacher_title': getattr(course.teacher, 'profile', {}).get('title', ''),
    }

    return render(request, 'Course-model.html', context)
