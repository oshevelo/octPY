from django.shortcuts import get_object_or_404


from rest_framework import generics, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, DjangoObjectPermissions
from django_filters.rest_framework import DjangoFilterBackend

from product.models import Product, ProductMedia, Characteristic
from product.serializers import ProductSerializer, ProductMediaSerializer, CharacteristicSerializer
from product.permissions import IsAdminOrReadOnly

class ProductMixin():
    
    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs.get('product_id'))
        return serializer.save(product=product)

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly,]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['categories', 'characteristics']
    ordering_fields = ['price', 'raiting']
    search_fields = ['name', 'price', 'raiting', 'categories']


    
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly,]
    
    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs.get('product_id'))

                                

class ProductMediaList(ProductMixin, generics.ListCreateAPIView):
    serializer_class = ProductMediaSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly,]
    
    def get_queryset(self):
        return ProductMedia.objects.filter(product_id=self.kwargs.get('product_id'))


class ProductMediaDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductMediaSerializer
    permission_classes = [IsAdminOrReadOnly,]

    def get_object(self):
        return get_object_or_404(ProductMedia, pk=self.kwargs.get('productmedia_id'))


class CharacteristicList(ProductMixin, generics.ListCreateAPIView):
    serializer_class = CharacteristicSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly,]
    
    def get_queryset(self):
        return Characteristic.objects.filter(product_id=self.kwargs.get('product_id'))


class CharacteristicDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CharacteristicSerializer
    permission_classes = [IsAdminOrReadOnly,]

    def get_object(self):
        return get_object_or_404(Characteristic, pk=self.kwargs.get('characteristic_id'))