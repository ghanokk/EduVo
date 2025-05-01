from django.contrib import admin
from .models import User, StudentProfile, TeacherProfile, CompanyProfile

admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(CompanyProfile)

# Register your models here.
