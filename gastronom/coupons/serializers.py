from rest_framework import serializers
from coupons.models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon

        fields = ('id', 'code', 'description', 'valid_from', 'valid_till', 'discount_value', 'created_at', 'updated_at', 'active')
        read_only_fields = ('id', 'created_at', 'updated_at')
