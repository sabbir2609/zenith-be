from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user has a related Staff object and if their role is "Manager"
        return (
            hasattr(request.user, "staff") and request.user.staff.role.name == "Manager"
        )


class IsReceptionist(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user has a related Staff object and if their role is "Receptionist"
        return (
            hasattr(request.user, "staff")
            and request.user.staff.role.name == "Receptionist"
        )


class IsHousekeeping(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user has a related Staff object and if their role is "Housekeeping"
        return (
            hasattr(request.user, "staff")
            and request.user.staff.role.name == "Housekeeping"
        )
