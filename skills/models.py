from django.db import models
from users.models import StudentProfile

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class UserSkill(models.Model):
    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    student_profile = models.ForeignKey(
        StudentProfile, 
        on_delete=models.CASCADE,
        related_name='skill_proficiencies'
    )
    skill = models.ForeignKey(
        Skill, 
        on_delete=models.CASCADE,
        related_name='student_proficiencies'
    )
    proficiency_level = models.CharField(
        max_length=12,
        choices=PROFICIENCY_CHOICES,
        default='beginner'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student_profile', 'skill')
    
    def __str__(self):
        return f"{self.student_profile.user.username} - {self.skill.name} ({self.get_proficiency_level_display()})"