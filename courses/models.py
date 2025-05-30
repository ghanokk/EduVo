from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']



class Course(models.Model):
    # had l'choices y3tina levels li n9dro n7tuhom fl cours (débutant, moyen, avancé...)
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('all levels', 'All Levels'),
    ]
    
    # had lchoices y3tina l'status t3 l'cours (msawd, mcharf, archivay)
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    # had lfields y7fed fihom l'information t3 lcourses
    title = models.CharField(max_length=255)  # lism t3 l'cours
    description = models.TextField()  # l'description  l'cours
    price = models.DecimalField(max_digits=10, decimal_places=2)  # l'prix dyal l'cours
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )  # l'catégorie dyal l'cours
    duration = models.CharField(max_length=100, blank=True, null=True)  # l'durée dyal l'cours
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)  # l'image dyal l'cours

    @property
    def image_url(self):
        try:
            if self.image and hasattr(self.image, 'url'):
                return self.image.url
            return '/static/assets/img/default-course.jpg'
        except ValueError:
            return '/static/assets/img/default-course.jpg'

    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Beginner')  # l'level dyal l'cours
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')  # l'status dyal l'cours
    teacher = models.ForeignKey(  # l'professeur li kay3lem l'cours
        'users.User',
        on_delete=models.CASCADE,
        related_name='taught_courses'
    )
    
    views = models.PositiveIntegerField(default=0)  # ch7al men wa7ed chaf l'cours
    created_at = models.DateTimeField(auto_now_add=True)  # l'date li t3mer fih l'cours
    updated_at = models.DateTimeField(auto_now=True)  # l'date li tbedel fih l'cours
    skills = models.ManyToManyField('skills.Skill', related_name='courses')  # l'skills li kay3tina f'l'cours
    objectives = models.TextField(blank=True)  # l'objectifs dyal l'cours
    prerequisites = models.TextField(blank=True)  # l'exigences préalables dyal l'cours
    cover_image = models.ImageField(upload_to='course_covers/', blank=True, null=True)  # l'image dyal l'cours
    creator = models.ForeignKey(User, on_delete=models.CASCADE)  # l'mostakhdim li khala9 l'cours
    def __str__(self):
        # hadi bach tban l'ism dyal l'cours f'l'admin w f'l'affichage
        return self.title

    def get_average_rating(self):
        """had l'fonction kay7seb l'moyenne dyal l'ratings dyal l'cours"""
        return self.ratings.aggregate(Avg('rating_value'))['rating_value__avg'] or 0

    def get_rating_count(self):
        """had l'fonction kay7seb ch7al men wa7ed 3ta rating l'l'cours"""
        return self.ratings.count()

    def get_enrollment_count(self):
        """had l'fonction kay7seb ch7al men étudiant dar inscription f'l'cours"""
        return self.enrollments.count()

    def get_total_lessons(self):
        """had l'fonction kay7seb ch7al men leçon kayn f'l'cours"""
        return Lesson.objects.filter(section__course=self).count()

    def get_total_duration(self):
        """had l'fonction kay7seb l'durée totale dyal l'cours"""
        total = Lesson.objects.filter(section__course=self).aggregate(
            total_duration=models.Sum('duration')
        )['total_duration']
        return total or self.duration or None

    class Meta:
        # hadi bach l'cours jdod ybanu l'awel
        ordering = ['-created_at']


class Section(models.Model):
    # had l'model kay7fed fih l'sections dyal l'cours
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)  # l'cours li kayn fih had l'section
    title = models.CharField(max_length=255)  # l'ism dyal l'section
    order = models.PositiveIntegerField(default=0)  # l'ordre dyal l'section f'l'cours

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        # hadi bach l'sections ybanu b'tartib
        ordering = ['order']
        # hadi bach ma ykonsh doublon f'l'ordre f'nfs l'cours
        unique_together = ('course', 'order')


class Lesson(models.Model):
    # had l'model kay7fed fih l'leçons dyal l'cours
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lessons')  # l'section li kayn fih had l'leçon
    title = models.CharField(max_length=255)  # l'ism dyal l'leçon
    video = models.FileField(upload_to='lesson_videos/', blank=True, null=True)  # l'vidéo dyal l'leçon
    content = models.TextField(blank=True, null=True)  # l'contenu dyal l'leçon
    duration = models.DurationField(blank=True, null=True)  # l'durée dyal l'leçon
    order = models.PositiveIntegerField(default=0)  # l'ordre dyal l'leçon f'l'section

    def __str__(self):
        return f"{self.section.course.title} - {self.title}"

    class Meta:
        # hadi bach l'leçons ybanu b'tartib
        ordering = ['order']
        # hadi bach ma ykonsh doublon f'l'ordre f'nfs l'section
        unique_together = ('section', 'order')


class Enrollment(models.Model):
    # had l'choices kay3tina l'status dyal l'inscription
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),  # dar inscription
        ('in_progress', 'In Progress'),  # kay dir l'cours
        ('completed', 'Completed'),  # kammel l'cours
    ]
    student = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completion_status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='enrolled')
    completion_date = models.DateTimeField(blank=True, null=True)
    progress = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    
    class Meta:
        # hadi bach l'étudiant ma ydirch inscription marra w7da f'nfs l'cours
        unique_together = ('student', 'course')
        # hadi bach l'inscriptions jdod ybanu l'awel
        ordering = ['-enrollment_date']


class Certificate(models.Model):
    student = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_file = models.FileField(upload_to='certificates/', null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title} Certificate"


class CourseProgress(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='course_progress')
    current_lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    certificate = models.OneToOneField(Certificate, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_progress')
    certificate_issued = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.enrollment.student.username} - {self.enrollment.course.title} Progress"


class Rating(models.Model):
    # had l'model kay7fed fih l'ratings dyal l'cours
    student = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='ratings')  # l'étudiant li 3ta l'rating
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')  # l'cours li 3ta lih l'rating
    rating_value = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # l'valeur dyal l'rating (1-5)
    comment = models.TextField(blank=True, null=True)  # l'commentaire dyal l'rating
    created_at = models.DateTimeField(auto_now_add=True)  # l'date li 3ta fih l'rating

    def __str__(self):
        return f"{self.rating_value} stars by {self.student.username} for {self.course.title}"

    def get_star_rating(self):
        """had l'fonction kay3tina l'stars bach n3rdo f'l'template"""
        return range(self.rating_value)

    class Meta:
        # hadi bach l'étudiant ma y3tich rating marra w7da l'nfs l'cours
        unique_together = ('student', 'course')
        # hadi bach l'ratings jdod ybanu l'awel
        ordering = ['-created_at']


class WhatYouLearn(models.Model):
    # had l'model kay7fed fih l'objectifs dyal l'cours
    course = models.ForeignKey(Course, related_name='what_you_learn', on_delete=models.CASCADE)  # l'cours
    description = models.TextField() # l'objectif li ghadi y3ref l'étudiant

    def __str__(self):
        return self.description


class Video(models.Model):
    section = models.ForeignKey(Section, related_name='videos', on_delete=models.CASCADE)
    file = models.FileField(upload_to='course_videos/')
    title = models.CharField(max_length=255, blank=True)


class CourseMaterial(models.Model):
    section = models.ForeignKey(Section, related_name='materials', on_delete=models.CASCADE)
    file = models.FileField(upload_to='course_materials/')
    title = models.CharField(max_length=255, blank=True)