from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group as AuthGroup
from .models import ProductAccess


class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.groups.filter(name__in=['teacher']).exists()


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class HasProductAccess(BasePermission):
    def has_object_permission(self, request, view, obj):
        return ProductAccess.objects.filter(user=request.user, product=obj).exists()