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
        fields = ['id', 'image']


class CharacteristicNestedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Characteristic
        fields = ['id', 'characteristic']


class ProductSerializer(serializers.ModelSerializer):
    media = MediaNestedSerializer(many=True, read_only=True)
    characteristics = CharacteristicNestedSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'descriptions', 'raiting', 'count', 'price', 'media']
        

class MediaSerializer(serializers.ModelSerializer):
    product = ProductNestedSerializer(read_only = True) 

    class Meta:
        model = Media
        fields = ['id', 'image', 'product']
        

class CharacteristicSerializer(serializers.ModelSerializer):
    product = ProductNestedSerializer(read_only = True)

    class Meta:
        model = Characteristic
        fields = ['id', 'characteristic', 'descriptions', 'product']
