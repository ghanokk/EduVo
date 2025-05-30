from django.contrib import admin
from .models import Skill, UserSkill

class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 1
    raw_id_fields = ['profile']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name', 'category']
    list_filter = ['category']
    inlines = [UserSkillInline]

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['profile', 'skill', 'proficiency_level', 'created_at']
    list_filter = ['proficiency_level', 'created_at']
    search_fields = ['profile__user__username', 'skill__name']
    raw_id_fields = ['profile', 'skill']