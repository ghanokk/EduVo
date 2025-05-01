from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)  # عنوان الوظيفة
    description = models.TextField()  # وصف الوظيفة
    posted_by = models.ForeignKey('users.User', on_delete=models.CASCADE)  # الشركة اللي ناضت الوظيفة
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ النشر

class Proposal(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  # الوظيفة
    freelancer = models.ForeignKey('users.User', on_delete=models.CASCADE)  # الشخص اللي قدم (طالب أو أستاذ)
    cover_letter = models.TextField()  # رسالة التقديم
    submitted_at = models.DateTimeField(auto_now_add=True)  # تاريخ التقديم

# Create your models here.
