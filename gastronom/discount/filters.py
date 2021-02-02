import django_filters
from discount.models import Discount_cart


class DiscountCartFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    valid_date_start = django_filters.DateTimeFromToRangeFilter()
    valid_date_end = django_filters.DateTimeFromToRangeFilter()
    
    class Meta:
        model = DiscountCart
        fields = ['code', 'valid_date_start', 'valid_date_end', 'status']
