from django.contrib import admin
from .models import (
    User, Profile, Course, Enrollment, Job, JobApplication,
    Payment, Skill, UserSkill, JobSkill, JobRecommendation,
    ModerationLog, Rating
)

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(Payment)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(JobSkill)
admin.site.register(JobRecommendation)
admin.site.register(ModerationLog)
admin.site.register(Rating)