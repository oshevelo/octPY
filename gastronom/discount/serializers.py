from rest_framework import serializers
from .models import *


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscountCart
        fields = ("cart", "code", "status")


class DiscountPostSerializer(serializers.Serializer):
    cart = serializers.IntegerField()
    code = serializers.CharField(max_length=200)
    amount_cart = serializers.DecimalField(max_digits=10, decimal_places=4)

