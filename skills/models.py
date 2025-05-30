from django.db import models
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)  # unique pour éviter les doublons genre "Python", "python"
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class UserSkill(models.Model):
    # skills is only for student and teacher profiles
    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    profile = models.ForeignKey(
        'users.Profile', 
        on_delete=models.CASCADE,
        related_name='skill_proficiencies'
    )
    skill = models.ForeignKey(
        Skill, 
        on_delete=models.CASCADE,
        related_name='profile_proficiencies'
    )
    proficiency_level = models.CharField(
        max_length=12,
        choices=PROFICIENCY_CHOICES,
        default='beginner'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('profile', 'skill')  # pour éviter que l’utilisateur ajoute la même skill deux fois

    def __str__(self):
        return f"{self.profile.user.username} - {self.skill.name} ({self.get_proficiency_level_display()})"