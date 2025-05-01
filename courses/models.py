from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)  # عنوان الكورس
    description = models.TextField()  # وصف الكورس
    teacher = models.ForeignKey('users.User', on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإنشاء

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # الكورس
    student = models.ForeignKey('users.User', on_delete=models.CASCADE)  # الطالب المسجل
    enrolled_at = models.DateTimeField(auto_now_add=True)  # تاريخ التسجيل



 # Create your models here.
