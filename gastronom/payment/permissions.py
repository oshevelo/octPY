from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import Payments, Status


class PaymentsPermission(BasePermission):
    def has_permission(self, request, view):
        obj = get_object_or_404(
            Payments,
            pk=view.kwargs.get('payment_id'),
            user = view.request.user
        )
        if request.method != 'GET':
            return obj.status == Status.submitted
        return obj