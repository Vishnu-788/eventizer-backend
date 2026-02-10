from rest_framework.permissions import BasePermission
from .enums import UserRoles


class IsHost(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRoles.HOST and request.user.verfied == True


class IsCustomAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRoles.ADMIN