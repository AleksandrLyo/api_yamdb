from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .models import User


class AuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = get_object_or_404(User, username=request.user.username)
        return user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        user = get_object_or_404(User, username=request.user.username)
        return user.role == 'admin'



