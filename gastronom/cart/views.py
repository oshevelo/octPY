from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartList(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all()


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(Cart,
                                pk=self.kwargs.get('cart_id'),
                                user=self.request.user, )
        return obj


class CartItemList(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = get_object_or_404(Cart,
                                 pk=self.kwargs.get('cart_item_id'),
                                 user=self.request.user, )
        return CartItem.objects.filter(user=self.request.user, cart=cart)


class CartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(CartItem,
                                pk=self.kwargs.get('cart_item_id'), )
        return obj
