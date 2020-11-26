from django.contrib.auth.models import User
from rest_framework import serializers
from product.models import Product, ProductMedia, Characteristic


class ProductNestedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku']

        
class ProductMediaNestedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductMedia
        fields = ['id', 'image']


class CharacteristicNestedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Characteristic
        fields = ['id', 'characteristic', 'descriptions']


class ProductSerializer(serializers.ModelSerializer):
    media = ProductMediaNestedSerializer(many=True, read_only=True)
    characteristics = CharacteristicNestedSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'descriptions', 'raiting', 'count', 'price', 'available', 'characteristics', 'media']
        

class ProductMediaSerializer(serializers.ModelSerializer):
    product = ProductNestedSerializer(read_only = True) 

    class Meta:
        model = ProductMedia
        fields = ['id', 'image', 'product']
        

class CharacteristicSerializer(serializers.ModelSerializer):
    product = ProductNestedSerializer(read_only = True)

    class Meta:
        model = Characteristic
        fields = ['id', 'characteristic', 'descriptions', 'product']
