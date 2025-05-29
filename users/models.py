from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# ✅ Classe principale des utilisateurs
# hadi t'étend l'utilisateur standard dyal Django (AbstractUser)
class User(AbstractUser):
    # You can keep user_type if you want a "main" role, or remove it for full flexibility
    is_freelancer = models.BooleanField(default=False) 


# ✅ Classe abstraite pour les profils (ta3 les users)
# hadi makhdamnach biha direct, mais les autres profils héritent menha
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")#to avoid clashes and make reverse lookups easier
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # photo profil
    bio = models.TextField(blank=True)  # un petit texte 3la l'utilisateur
    created_at = models.DateTimeField(default=timezone.now)  # date de création
    country = models.CharField(max_length=10, blank=True)  # <-- ADD THIS LINE
    wilaya = models.CharField(max_length=50, blank=True)  
    
    # Role flags
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)

    # Student/Teacher fields
    is_freelancer = models.BooleanField(default=False)  
    skills = models.ManyToManyField('skills.Skill', through='skills.UserSkill', blank=True)

    # Teacher fields
    expertise = models.TextField(blank=True)
    reputation_score = models.IntegerField(default=0)
    # Company fields
    company_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    company_image = models.ImageField(upload_to='company_pics/', blank=True, null=True)

    def get_full_name(self):
        return self.user.get_full_name() or self.user.username

    def get_location(self):
        return self.country or "Not set"

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
