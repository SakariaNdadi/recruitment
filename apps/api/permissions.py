from rest_framework import permissions

class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.user_type == "admin" and request.user.is_authenticated