from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAuthorStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user == obj.author
                         or (request.user.is_moderator
                             and request.method == 'DELETE')
                         or request.user.is_admin
                         or request.user.is_superuser
                         )))


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin
                                                  or request.user.is_superuser)
