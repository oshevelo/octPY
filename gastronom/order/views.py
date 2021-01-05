from django.shortcuts import render

from order.models import Order
from order.serializers import OrderSerializer, OrderDetailSerializer

from rest_framework import generics
from django.shortcuts import get_object_or_404


class OrdersList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderDetailSerializer

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs.get('order_id'))
