from django.contrib.auth.models import User
from rest_framework import serializers
import drf_writable_nested

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'is_sent', 'sent_time', 'source', 'recipient', 'message', 'timestamp', 'send_method']


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class NotificationNestedSerializer(drf_writable_nested.WritableNestedModelSerializer):
    notifications = NotificationSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'notifications']
