from rest_framework.permissions import BasePermission
from .enums import UserRoles


class IsHost(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == UserRoles.HOST

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == UserRoles.ADMIN