import logging

from django.http import HttpResponse
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


class NotificationsByUserNested(generics.RetrieveUpdateDestroyAPIView):
    """
    Outputs notifications by recipient id nested. Path = 'notifications/recipient/<int:recipient_id>/nested'
    """
    serializer_class = NotificationNestedSerializer

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('recipient_id'))


def index(request):
    return HttpResponse("Hello logging world.")


logger = logging.getLogger('__name__')

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})
