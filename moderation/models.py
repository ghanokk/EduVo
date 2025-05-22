from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ModerationLog(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('course', 'Course'),
        ('job', 'Job'),
        ('profile', 'Profile'),
    ]

    ACTION_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('flagged', 'Flagged'),
    ]

    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    content_id = models.IntegerField()
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    reason = models.TextField(blank=True, null=True)
    action_date = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content_type} #{self.content_id} - {self.action}"

# Create your models here.
