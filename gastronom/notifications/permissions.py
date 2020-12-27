from rest_framework.permissions import BasePermission, SAFE_METHODS
from notifications.errors import CustomForbidden


class ReadOnlyOrFull(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff and request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        else:
            raise CustomForbidden

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff and request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        else:
            raise CustomForbidden
