from django.shortcuts import get_object_or_404
from rest_framework import permissions

from django.contrib.auth import get_user_model

User = get_user_model()


class IsAuthorStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # user = get_object_or_404(User, username=request.user.username)
        if request.user.role == 'moderator':
            return request.method == 'DELETE'
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user or request.user.role == 'admin')


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # user = get_object_or_404(User, username=request.user.username)
        return (request.method in permissions.SAFE_METHODS or
                request.user.role == 'admin')


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # user = get_object_or_404(User, username=request.user.username)
        return request.user.role == 'admin'
