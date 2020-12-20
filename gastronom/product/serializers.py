from django.contrib.auth.models import User
from rest_framework import serializers
from product.models import Product, ProductMedia, Characteristic
from catalog.serializers import CatalogDetailedSerializer


class ProductNestedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku']

        
class ProductMediaNestedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductMedia
        fields = ['id', 'medium_image']


class CharacteristicNestedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Characteristic
        fields = ['id', 'characteristic', 'descriptions']


class ProductSerializer(serializers.ModelSerializer):
    image = ProductMediaNestedSerializer(many=True, read_only=True)
    characteristics = CharacteristicNestedSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'sku', 'descriptions', 'categories', 'raiting', 'count', 'price', 'available', 'characteristics']
        

class ProductMediaSerializer(serializers.ModelSerializer):
    product = ProductNestedSerializer(read_only = True) 

    class Meta:
        model = ProductMedia
        fields = '__all__'
        

class CharacteristicSerializer(serializers.ModelSerializer):
    product = ProductNestedSerializer(read_only = True)

    class Meta:
        model = Characteristic
        fields = ['id', 'characteristic', 'descriptions', 'product']
