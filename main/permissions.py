from rest_framework import permissions


class IsGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "guest")
