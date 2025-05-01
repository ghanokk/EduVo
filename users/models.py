from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # أنواع المستخدمين
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  #yetna7a koulch met3l9 bl user ida na7it m user
    bio = models.TextField(blank=True)  # السيرة الذاتية
    skills = models.JSONField(default=list)  # المهارات

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expertise = models.TextField(blank=True)  # التخصص
    bio = models.TextField(blank=True)  # السيرة الذاتية
    reputation_score = models.IntegerField(default=0)

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)  # اسم الشركة
    description = models.TextField()  # وصف الشركة


 # Create your models here.
