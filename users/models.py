# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Wilaya choices
WILAYA_CHOICES = [
    ('0', 'Blida'),
    ('1', 'Adrar'),
    ('2', 'Chlef'),
    ('3', 'Laghouat'),
    ('4', 'Oum El Bouaghi'),
    ('5', 'Batna'),
    ('6', 'Béjaïa'),
    ('7', 'Biskra'),
    ('8', 'Béchar'),
    ('9', 'Blida'),
    ('10', 'Bouira'),
    ('11', 'Tamanrasset'),
    ('12', 'Tébessa'),
    ('13', 'Tlemcen'),
    ('14', 'Tiaret'),
    ('15', 'Tizi Ouzou'),
    ('16', 'Alger'),
    ('17', 'Djelfa'),
    ('18', 'Jijel'),
    ('19', 'Sétif'),
    ('20', 'Saïda'),
    ('21', 'Skikda'),
    ('22', 'Sidi Bel Abbès'),
    ('23', 'Annaba'),
    ('24', 'Guelma'),
    ('25', 'Constantine'),
    ('26', 'Médéa'),
    ('27', 'Mostaganem'),
    ('28', 'M’Sila'),
    ('29', 'Mascara'),
    ('30', 'Ouargla'),
    ('31', 'Oran'),
    ('32', 'El Bayadh'),
    ('33', 'Illizi'),
    ('34', 'Bordj Bou Arréridj'),
    ('35', 'Boumerdès'),
    ('36', 'El Tarf'),
    ('37', 'Tindouf'),
    ('38', 'Tissemsilt'),
    ('39', 'El Oued'),
    ('40', 'Khenchela'),
    ('41', 'Souk Ahras'),
    ('42', 'Tipaza'),
    ('43', 'Mila'),
    ('44', 'Aïn Defla'),
    ('45', 'Naâma'),
    ('46', 'Aïn Témouchent'),
    ('47', 'Ghardaïa'),
    ('48', 'Relizane'),
    ('49', 'Timimoun'),
    ('50', 'Bordj Badji Mokhtar'),
    ('51', 'Ouled Djellal'),
    ('52', 'Béni Abbès'),
    ('53', 'In Salah'),
    ('54', 'In Guezzam'),
    ('55', 'Touggourt'),
    ('56', 'Djanet'),
    ('57', 'El M Ghair'),
    ('58', 'El Meniaa'),
]

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
    wilaya = models.CharField(max_length=2, choices=WILAYA_CHOICES, blank=True)  # wilaya of the user
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
    image = models.ImageField(upload_to='company_pics/', blank=True, null=True)
    country=models.CharField(max_length=10,null=False)
    