from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.staff.role.name == "Manager"
        )


class IsReceptionist(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.staff.role.name == "Receptionist"
        )


class IsHousekeeping(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.staff.role.name == "Housekeeping"
        )
