from rest_framework.serializers import ModelSerializer
from .models import Cart, CartItem


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'creation_date', ]


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'unit_price', 'total_price', ]
