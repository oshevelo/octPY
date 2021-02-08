import django_filters
from django.db.models import Q
from .models import Payments, status_list, paymentsystem_list


class PaymentsFilter(django_filters.FilterSet):

    def user_contains(self, qs, contains, value):
        lookup = Q(user__email__icontains=value) | \
                 Q(user__username__icontains=value)
        return qs.filter(lookup)

    def date_contains(self, qs, contains, value):
        lookup = Q(payment_date__icontains=value)
        return qs.filter(lookup)

    user = django_filters.filters.CharFilter(method='user_contains')
    payment_date = django_filters.filters.CharFilter(method='date_contains')
    id = django_filters.NumberFilter()
    billAmount = django_filters.NumberFilter()
    paymentsystem = django_filters.filters.ChoiceFilter(
        choices=paymentsystem_list
    )

    status = django_filters.filters.ChoiceFilter(
        choices=status_list
    )

    class Meta:
        model = Payments
        fields = [
            'id',
            'user',
            'billAmount',
            'paymentsystem',
            'payment_date',
            'status',
        ]