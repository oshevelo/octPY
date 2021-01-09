import django_filters
from notifications.models import Notification


class NotificationFilter(django_filters.FilterSet):
    sent_time = django_filters.DateTimeFromToRangeFilter()
    message = django_filters.CharFilter(lookup_expr='icontains')
    timestamp = django_filters.OrderingFilter()

    class Meta:
        model = Notification
        fields = ['subject', 'message', 'send_method', 'source', 'is_sent', 'timestamp']
