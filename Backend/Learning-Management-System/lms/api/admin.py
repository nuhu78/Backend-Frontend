from django.contrib import admin
from .models import Teacher, Student, Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']
admin.site.register(Teacher)
admin.site.register(Student)
# `Profile` is already registered via the `@admin.register(Profile)` decorator above.
# Removed the duplicate registration to avoid AlreadyRegistered error.
