from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ModerationLog(models.Model):
    # types d'actions li ydirha l'admin
    ACTION_CHOICES = [
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('ban_user', 'User Banned'),
        ('delete_content', 'Content Deleted'),
        ('warn_user', 'User Warned'),
    ]

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)  # wesh dar l'admin
    target_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='moderated_logs'
    )  # utilisateur concerné (ex: teacher, student...)
    
    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='moderation_actions'
    )  # admin/modérateur li dar l'action

    reason = models.TextField(blank=True, null=True)  # 3lach dar l'action (facultatif)

    timestamp = models.DateTimeField(default=timezone.now)  # date li dar l'action

    related_object = models.CharField(
        max_length=255,
        blank=True
    )  # contenu concerné (ex: job#2, course#5)

    class Meta:
        ordering = ['-timestamp']  # yban l'action ml lakher lewl 
        verbose_name = 'Journal de modération'
        verbose_name_plural = 'Journaux de modération'

    def __str__(self):
        return f"{self.get_action_display()} - {self.target_user} by {self.performed_by}"