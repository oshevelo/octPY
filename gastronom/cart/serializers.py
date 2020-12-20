from rest_framework.serializers import ModelSerializer
from .models import Cart, CartItem


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'unit_price', 'amount_left', ]


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'creation_date', 'total_price', 'cart_items', ]

    cart_items = CartItemSerializer(many=True, read_only=True)
