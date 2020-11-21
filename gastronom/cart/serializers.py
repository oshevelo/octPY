from rest_framework import serializers
from .models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'creation_date']


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        # fields = ['cart', 'product', 'quantity', 'price', 'creation_date', ]
        fields = ['cart', 'quantity', 'price', 'creation_date', ]
