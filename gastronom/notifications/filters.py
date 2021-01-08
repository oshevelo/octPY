import django_filters
from notifications.models import Notification


class NotificationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Notification
        fields = ['subject', 'message', 'send_method', 'source']
