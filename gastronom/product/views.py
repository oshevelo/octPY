from django.shortcuts import get_object_or_404


from rest_framework import generics, filters
from rest_framework.pagination import LimitOffsetPagination

from product.models import Product, ProductMedia, Characteristic
from product.serializers import ProductSerializer, ProductMediaSerializer, CharacteristicSerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['price', 'raiting']
    search_fields = ['name', 'price', 'raiting']


    
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    
    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs.get('product_id'))
                                

class ProductMediaList(generics.ListCreateAPIView):
    serializer_class = ProductMediaSerializer
    
    def get_queryset(self):
        return ProductMedia.objects.filter(product_id=self.kwargs.get('product_id'))


class CharacteristicList(generics.ListCreateAPIView):
    serializer_class = CharacteristicSerializer
    
    def get_queryset(self):
        return Characteristic.objects.filter(product_id=self.kwargs.get('product_id'))
