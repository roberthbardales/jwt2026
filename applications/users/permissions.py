from rest_framework.permissions import BasePermission
from .models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.occupation == User.ADMINISTRADOR


class IsAdminOrEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.occupation in [
            User.ADMINISTRADOR, User.EMPLEADO
        ]


class IsAdminOrClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.occupation in [
            User.ADMINISTRADOR, User.CLIENTE
        ]
