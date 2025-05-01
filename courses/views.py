from django.shortcuts import render
from .models import Course

def courses_page(request):
    top_courses = Course.objects.all().order_by('-rating')[:4]  # Top 4 rated courses
    all_courses = Course.objects.all()
    return render(request, 'courses.html', {
        'top_courses': top_courses,
        'all_courses': all_courses
    })

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})
# Create your views here.
