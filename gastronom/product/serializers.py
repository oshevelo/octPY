from django.contrib.auth.models import User
from rest_framework import serializers
from product.models import Product, Media, Characteristic


class ProductNestedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku']

        
class MediaNestedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Media
        fields = ['id', 'product_image']


class CharacteristicNestedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Characteristic
        fields = ['id', 'characteristic', 'descriptions']


class ProductSerializer(serializers.ModelSerializer):
    images = MediaNestedSerializer(many=True, read_only=True)
    characteristics = CharacteristicNestedSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'descriptions', 'raiting', 'count', 'price', 'available', 'characteristics', 'images']
        

class MediaSerializer(serializers.ModelSerializer):
    product = ProductNestedSerializer(read_only = True) 

    class Meta:
        model = Media
        fields = ['id', 'product_image', 'product']
        

class CharacteristicSerializer(serializers.ModelSerializer):
    product = ProductNestedSerializer(read_only = True)

    class Meta:
        model = Characteristic
        fields = ['id', 'characteristic', 'descriptions', 'product']
