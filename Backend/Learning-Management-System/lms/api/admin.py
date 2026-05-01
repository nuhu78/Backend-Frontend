from django.contrib import admin
from .models import Enrollment, Teacher, Student, Profile, Course, CourseCategory

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']
admin.site.register(Teacher)
admin.site.register(Student)


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'instructor', 'category', 'level', 'is_published']
    list_filter = ['level', 'is_published', 'category']
    search_fields = ['title', 'description']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'enrolled_at', 'is_active']
    list_filter = ['is_active', 'enrolled_at']
# `Profile` is already registered via the `@admin.register(Profile)` decorator above.
# Removed the duplicate registration to avoid AlreadyRegistered error.
