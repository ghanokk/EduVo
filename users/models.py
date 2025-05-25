from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# ✅ Classe principale des utilisateurs
# hadi t'étend l'utilisateur standard dyal Django (AbstractUser)
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),   # 👨‍🎓 étudiant
        ('teacher', 'Teacher'),   # 👨‍🏫 enseignant
        ('company', 'Company'),   # 🏢 entreprise
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_freelancer = models.BooleanField(default=False) 


    # ✅ Fonction pour retourner le bon profil selon le type
    def get_profile(self):
        if self.user_type == 'student':
            return self.studentprofile  # wch user student, rj3 profil ta3 étudiant
        elif self.user_type == 'teacher':
            return self.teacherprofile  # wch prof, rj3 profil ta3 prof
        elif self.user_type == 'company':
            return self.companyprofile  # wch entreprise, rj3 profil entreprise
        return None


# ✅ Classe abstraite pour les profils (ta3 les users)
# hadi makhdamnach biha direct, mais les autres profils héritent menha
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # chaque user andou profil unique
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # photo profil
    bio = models.TextField(blank=True)  # un petit texte 3la l'utilisateur
    created_at = models.DateTimeField(default=timezone.now)  # date de création

    class Meta:
        abstract = True  # 👈 ma ttsajelch f la base directement

# ✅ Profil étudiant
class StudentProfile(Profile):
    skills = models.ManyToManyField('skills.Skill', through='skills.UserSkill')  # les compétences ta3 l'étudiant
    is_freelancer = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}'s Student Profile"

# ✅ Profil prof
class TeacherProfile(Profile):
    expertise = models.TextField(blank=True)  # domaine d'expertise
    reputation_score = models.IntegerField(default=0)  # note de réputation (tbda 0)
    is_freelancer = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}'s Teacher Profile"

# ✅ Profil entreprise
class CompanyProfile(Profile):
    company_name = models.CharField(max_length=255)  # nom ta3 la société
    description = models.TextField()  # un petit résumé 3la la boîte
    