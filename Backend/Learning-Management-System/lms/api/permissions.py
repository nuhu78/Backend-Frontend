from rest_framework import permissions


def get_user_role(user):
    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return 'ADMIN'

    if hasattr(user, 'profile'):
        return user.profile.role

    return None


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == 'ADMIN'


class IsInstructorRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == 'INSTRUCTOR'


class IsStudentRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == 'STUDENT'


class IsAdminOrInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) in ['ADMIN', 'INSTRUCTOR']


class IsCourseOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        role = get_user_role(request.user)

        if role == 'ADMIN':
            return True

        if role == 'INSTRUCTOR':
            return obj.instructor == request.user

        return False


class IsEnrollmentOwnerOrAdminOrInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        role = get_user_role(request.user)

        if role == 'ADMIN':
            return True

        if role == 'INSTRUCTOR':
            return obj.course.instructor == request.user

        if role == 'STUDENT':
            return obj.student == request.user

        return False