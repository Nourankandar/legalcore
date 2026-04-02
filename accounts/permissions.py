from rest_framework import permissions

from accounts.models import User

class IsAdminOrLawyer(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return request.user and request.user.is_authenticated and(
            request.user.role ==User.ADMIN or request.user.role == User.LAWYER
        )