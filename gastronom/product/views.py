from django.shortcuts import get_object_or_404

from rest_framework import generics

from product.models import Product, Media, Characteristic
from product.serializers import ProductSerializer, MediaSerializer, CharacteristicSerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    
    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs.get('product_id'))
                                

class MediaList(generics.ListAPIView):
    serializer_class = MediaSerializer
    
    def get_queryset(self):
        return Media.objects.filter(product_id=self.kwargs.get('product_id'))


class CharacteristicList(generics.ListCreateAPIView):
    serializer_class = CharacteristicSerializer
    
    def get_queryset(self):
        return Characteristic.objects.filter(product_id=self.kwargs.get('product_id'))

# TODO ProductView, How many producs was sell, comparison of products, while taking into account that the products must be in the same category, add sort by sku, search by sku(admin.py), sort by price (from cheap to expensive and reverse)
