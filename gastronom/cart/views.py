from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartDetailSerializer, CartItemSerializer


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()

    def get_object(self):
        return get_object_or_404(Cart, pk=self.kwargs.get('cart_id'), user=self.request.user)


class CartItemList(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = get_object_or_404(Cart,
                                pk=self.kwargs.get('cart_id'),
                                user=self.request.user)
        return CartItem.objects.filter(user=self.request.user, cart=cart)


class CartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart_item = get_object_or_404(CartItem, pk=self.kwargs.get('cart_item_id'))
        return cart_item
