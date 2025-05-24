from django.contrib import admin
from .models import Course, Section, Lesson, Enrollment, Rating, WhatYouLearn

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'price', 'category', 'level', 'get_rating', 'get_student_count', 'created_at')
    list_filter = ('category', 'level', 'status', 'created_at')
    search_fields = ('title', 'description', 'teacher__username')
    readonly_fields = ('get_rating', 'get_student_count', 'views', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'teacher', 'price', 'category', 'level')
        }),
        ('Course Details', {
            'fields': ('duration', 'skills')
        }),
        ('Media', {
            'fields': ('image', 'video')
        }),
        ('Statistics', {
            'fields': ('get_rating', 'get_student_count', 'views')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-created_at',)

    def get_rating(self, obj):
        return obj.get_average_rating()
    get_rating.short_description = 'Rating'

    def get_student_count(self, obj):
        return obj.get_enrollment_count()
    get_student_count.short_description = 'Students'

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ('course', 'order')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'duration', 'order')
    list_filter = ('section__course', 'section')
    search_fields = ('title', 'section__title', 'section__course__title')
    ordering = ('section', 'order')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'completion_status')
    list_filter = ('completion_status', 'enrollment_date')
    search_fields = ('student__username', 'course__title')
    readonly_fields = ('enrollment_date',)
    ordering = ('-enrollment_date',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating_value', 'created_at')
    list_filter = ('rating_value', 'created_at')
    search_fields = ('student__username', 'course__title', 'comment')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(WhatYouLearn)
class WhatYouLearnAdmin(admin.ModelAdmin):
    list_display = ('course',)
    list_filter = ('course',)
    search_fields = ('text', 'course__title')
    ordering = ('course',)