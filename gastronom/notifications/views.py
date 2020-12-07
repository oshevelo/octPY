from django.shortcuts import get_list_or_404
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from notifications.models import Notification
from notifications.serializers import NotificationSerializer, NotificationNestedSerializer


class NotificationListCreate(generics.ListCreateAPIView):
    """
    Outputs last 50 notifications from db. Path = 'notifications/last/'
    """
    queryset = Notification.objects.order_by('-timestamp')[:50]
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination


class NotificationsByRecipient(generics.ListCreateAPIView):
    """
    Outputs notifications by recipient id. Path = 'notifications/recipient/<int:recipient_id>/'
    """
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        obj = get_list_or_404(Notification, recipient=self.kwargs.get('recipient_id'))
        return obj


class NotificationsByUserNested(generics.RetrieveUpdateDestroyAPIView):
    """
    Outputs notifications by recipient id nested. Path = 'notifications/recipient/<int:recipient_id>/nested'
    """
    serializer_class = NotificationNestedSerializer
    pagination_class = LimitOffsetPagination

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('recipient_id'))


class NotificationsUnsent(generics.ListCreateAPIView):
    """
    Outputs unsent notifications. Path = 'notifications/unsent'
    """
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        lst = get_list_or_404(Notification, sent=False)
        return lst
