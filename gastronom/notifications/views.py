from django.shortcuts import get_list_or_404
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.generics import get_object_or_404

from notifications.models import Notification
from notifications.serializers import NotificationSerializer, NotificationNestedSerializer


class NotificationListCreate(generics.ListCreateAPIView):
    """
    Outputs last 50 notifications from db. Path = 'notifications/last/'
    """
    queryset = Notification.objects.order_by('-timestamp')[:50]
    serializer_class = NotificationSerializer


class NotificationsByRecipient(generics.ListCreateAPIView):
    """
    Outputs notifications by recipient id. Path = 'notifications/recipient/<int:recipient_id>/'
    """
    serializer_class = NotificationSerializer

    def get_queryset(self):
        obj = get_list_or_404(Notification, recipient=self.kwargs.get('recipient_id'))
        return obj


class QuestionChoiceNested(generics.RetrieveUpdateDestroyAPIView):
    """
    Outputs notifications by recipient id nested. Path = 'notifications/recipient/<int:recipient_id>/nested'
    """
    serializer_class = NotificationNestedSerializer

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('recipient_id'))
