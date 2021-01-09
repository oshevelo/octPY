import logging

# import django_filters
import django_filters
from django.shortcuts import get_list_or_404
from django.contrib.auth.models import User

from rest_framework import filters
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from gastronom.settings import USE_QUEUE
from notifications.models import Notification
from notifications.serializers import NotificationSerializer, NotificationNestedSerializer
from notifications.tasks import send_methods
from notifications.permissions import ReadOnlyOrFull


logger = logging.getLogger(__name__)


class NotificationAll(generics.ListCreateAPIView):
    """
    Outputs all notifications from db with available filtration. Path = 'notifications/all/'.
    """
    queryset = Notification.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['is_sent', 'timestamp']
    filterset_fields = ['recipient', 'is_sent', 'send_method', 'message', 'source', 'subject']
    search_fields = ['send_method', 'message', 'source', 'subject']

    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [ReadOnlyOrFull]


class NotificationListCreate(generics.ListCreateAPIView):
    """
    Outputs last 50 notifications from db. Path = 'notifications/last/'
    """
    queryset = Notification.objects.order_by('-timestamp')[:50]
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [ReadOnlyOrFull]


class NotificationsByRecipient(generics.ListCreateAPIView):
    """
    Outputs notifications by recipient id. Path = 'notifications/recipient/<int:recipient_id>/'
    """
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [ReadOnlyOrFull]

    def get_queryset(self):
        obj = get_list_or_404(Notification, recipient=self.kwargs.get('recipient_id'))
        return obj


class NotificationsByUserNested(generics.RetrieveUpdateDestroyAPIView):
    """
    Outputs notifications by recipient id nested. Path = 'notifications/recipient/<int:recipient_id>/nested'
    """
    serializer_class = NotificationNestedSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [ReadOnlyOrFull]

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('recipient_id'))


class NotificationsUnsent(generics.ListCreateAPIView):
    """
    Outputs unsent notifications. Path = 'notifications/unsent'
    """
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [ReadOnlyOrFull]

    def get_queryset(self):
        lst = get_list_or_404(Notification, is_sent=False)
        return lst


def create_notifications(source, recipients, message, send_method='email', subject='GASTRONOM info'):
    """
    Create and save notification objects to database
    :param source: str, name of app making notification
    :param recipients: list of class User objects
    :param subject: str, subject of notification
    :param message: str, body of notification message
    :param send_method: str, name of send method
    Examples:
from django.contrib.auth.models import User
from notifications.models import Notification
from user_profile.models import UserProfile
    email to list of Users:
Notification.create_notifications('notifications', recipients=[User.objects.get(id=1), User.objects.get(id=4)], message='This is my 100500th e-mail notification from Django.gastronom', send_method='email', subject='My 100500 message')
    telegram to list of Users:
Notification.create_notifications('notifications', recipients=[User.objects.get(id=1), User.objects.get(id=4)], message='This is my 100500th e-mail notification from Django.gastronom', send_method='email', subject='My 100500 message')
    telegram to all Users:
Notification.create_notifications('notifications', recipients=[user for user in User.objects.all()], message='Це моя перша телеграма from Django.gastronom', send_method='telegram')
    """
    if send_method in send_methods:
        send_func = send_methods[send_method]
        for user in recipients:
            notification = Notification(source=source, recipient=user, subject=subject, message=message, send_method=send_method)
            notification.save()
            if USE_QUEUE:
                send_func.delay(notification.id)
            else:
                send_func(notification.id)
    else:
        logger.error('Invalid send method passed to the create_notifications')
