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


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class IsAdminOrReservationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.reservation.user == request.user


class IsAdminOrInstallmentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.installment.reservation.user == request.user
