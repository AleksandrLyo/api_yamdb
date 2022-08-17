from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .models import User


class IsAuthorStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = get_object_or_404(User, username=request.user.username)
        if user.role == 'moderator':
            return request.method == 'DELETE'
        return (request.method in permissions.SAFE_METHODS
                or obj.author == user or user.role == 'admin')


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = get_object_or_404(User, username=request.user.username)
        return (request.method in permissions.SAFE_METHODS or
                user.role == 'admin')


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = get_object_or_404(User, username=request.user.username)
        return user.role == 'admin'
