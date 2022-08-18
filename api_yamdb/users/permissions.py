from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAuthorStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'moderator':
            return request.method == 'DELETE'
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user or request.user.role == 'admin')


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                request.user.role == 'admin' or request.user.is_staff is True)


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == 'admin' or
                    request.user.is_superuser is True)
