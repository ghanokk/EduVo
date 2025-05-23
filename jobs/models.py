from django.db import models

class Job(models.Model):
    STATUS_CHOICES = [
    ('open', 'Open'),
    ('closed', 'Closed'),
    ('draft', 'Draft'),
]
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('design', 'Graphic Design'),
        ('data', 'Data Entry'),
        ('writing', 'Content Writing'),
        ('marketing', 'Marketing'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=255)  # عنوان الوظيفة
    description = models.TextField()  # وصف الوظيفة
    posted_by = models.ForeignKey('users.User', on_delete=models.CASCADE)  # الشركة اللي ناضت الوظيفة
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ النشر
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
#Pourquoi ? T9der tkoun khdemt 3la job mais mazel ma publicatehach (draft), oula skartha (closed).
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')  # نوع الوظيفة

    def __str__(self):
        return f"{self.title} - {self.posted_by.username}"

    class Meta:
        ordering = ['-created_at']  # Yban l'offre mel lakher l lewl


class Proposal(models.Model):
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  # الوظيفة
    freelancer = models.ForeignKey('users.User', on_delete=models.CASCADE)  # الشخص اللي قدم (طالب أو أستاذ)
    cover_letter = models.TextField()  # رسالة التقديم
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)  # السيرة الذاتية
    submitted_at = models.DateTimeField(auto_now_add=True)  # تاريخ التقديم
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.freelancer.username} - {self.job.title}"
    class Meta:
         ordering = ['-submitted_at']


# Create your models here.
