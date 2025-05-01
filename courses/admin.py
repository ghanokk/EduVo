from django.contrib import admin
from .models import Course, Enrollment  

#Note : Just For Better Decorate
@admin.register(Course) 
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at')  
    search_fields = ('title', 'description')  
    list_filter = ('created_at',) 

admin.site.register(Enrollment)