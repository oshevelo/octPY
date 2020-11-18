from django.shortcuts import render
# from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartList(generics.ListAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class CartDetail(generics.ListCreateAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs.get('cart_id'))


class CartItemDetail(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.filter()  # <---- ?

    def get_object(self):
        return get_object_or_404(CartItem, pk=self.kwargs.get('cart_item_id'))
