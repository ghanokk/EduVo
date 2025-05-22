from django.contrib import admin
from .models import Skill, UserSkill

class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 1
    raw_id_fields = ['student_profile']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name', 'category']
    list_filter = ['category']
    inlines = [UserSkillInline]

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['student_profile', 'skill', 'proficiency_level', 'created_at']
    list_filter = ['proficiency_level', 'created_at']
    search_fields = ['student_profile__user__username', 'skill__name']
    raw_id_fields = ['student_profile', 'skill']



# from django.contrib import admin
# from .models import Skill, UserSkill

# class UserSkillInline(admin.TabularInline):
#     model = UserSkill
#     extra = 1
#     raw_id_fields = ['user']   #  user yban b id 

# @admin.register(Skill)
# class SkillAdmin(admin.ModelAdmin):
#     list_display = ['name', 'category']
#     search_fields = ['name', 'category']
#     list_filter = ['category']  #N9dro nfiltriw lista b7al fi kategoriat l-skill
#     inlines = [UserSkillInline] #Kaydkhl lina UserSkillInline f l-page dyal skill bach n9dro zidou l-skills m3a l-users direct men l-page dyal skill.

# @admin.register(UserSkill)
# class UserSkillAdmin(admin.ModelAdmin):
#     list_display = ['user', 'skill', 'proficiency_level', 'created_at'] #Hadchi kay3tina l-possibilité bach nchofo l-user, skill, level dyal proficiency w tarikhs dyal l-insertion direct fi la liste dyal l-admin.
#     list_filter = ['proficiency_level', 'created_at']#N9dro nfiltriw b7al m3a niveau dyal proficiency wala tari5 dyal 
#     search_fields = ['user__username', 'skill__name'] #: Katdir lina l-b7th fi username dyal l-user w smiya dyal skill.
#     raw_id_fields = ['user', 'skill'] #Hadi kaydkhl lina ID raw mn l-user w skill b7al l-UserSkillInline.