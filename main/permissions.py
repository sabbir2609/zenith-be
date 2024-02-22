from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow full access to administrators and read-only access to others.
    """

    def has_permission(self, request, view):
        # Allow read-only access for non-admin users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow full access for admin users
        return request.user and request.user.is_staff


class IsAdminOrStaffUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow full access to superusers and staff users, read-only access to others.
    """

    def has_permission(self, request, view):
        # Allow read-only access for non-admin and non-staff users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow full access for superusers and staff users
        return request.user and (
            request.user.is_superuser or request.user.staff.exists()
        )


class IsReservationOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow access to reservation owners and admins only.
    """

    def has_object_permission(self, request, view, obj):
        # Allow access to admins
        if request.user and request.user.is_superuser:
            return True

        # Allow access to reservation owner
        return obj.user == request.user
