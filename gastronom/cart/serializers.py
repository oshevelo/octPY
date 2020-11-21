from rest_framework.serializers import ModelSerializer
from .models import Cart, CartItem


class CartDetailSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'creation_date']


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'quantity', 'unit_price', 'total_price', 'creation_date', ]


class CartItemDetailSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'quantity', 'unit_price', 'total_price', 'creation_date', ]
