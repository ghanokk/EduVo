from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)  # عنوان الكورس
    description = models.TextField()  # وصف الكورس
    teacher = models.ForeignKey('users.User', on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإنشاء

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    image = models.ImageField(
    upload_to='course_images/',
    null=True,          # Allows NULL in database
    blank=True,         # Allows blank in forms
)
    # video = models.FileField(upload_to='course_videos/', null=True, blank =True)
    # category = models.CharField(max_length=100, default='general')  # Tnajem tbadel valeur par défaut kima t7eb
    # level = models.CharField(max_length=50, null=True, blank =True)  
    # rating = models.FloatField(default=0)  
    # is_free = models.BooleanField(default=False)  # Add this line
    # students = models.ManyToManyField(          # Add this relationship
    #     'users.User', 
    #     through='Enrollment',
    #     related_name='enrolled_courses'
    # )


class Enrollment(models.Model):
    student = models.ForeignKey('users.User', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

#  class Meta:
#         unique_together = [['student', 'course']]  # Prevent duplicate enrollments

 # Create your models here.
