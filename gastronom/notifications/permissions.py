from rest_framework import status
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import APIException


class ReadOnlyOrFull(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff and request.method in SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        else:
            raise CustomForbidden

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff and request.method in SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        else:
            raise CustomForbidden


class CustomForbidden(APIException):
    status_code = status.HTTP_404_NOT_FOUND
