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
        fields = ['id', 'thumbnail_image', 'medium_image']


class CharacteristicNestedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Characteristic
        fields = ['id', 'characteristic', 'descriptions']


class ProductSerializer(serializers.ModelSerializer):
    mediafiles = ProductMediaNestedSerializer(many=True, read_only=True)
    characteristics = CharacteristicNestedSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'categories', 'mediafiles', 'sku', 'descriptions', 'raiting', 'productcount', 'price', 'available', 'characteristics']
        

class ProductMediaSerializer(serializers.ModelSerializer):
    product = ProductNestedSerializer(read_only = True) 

    class Meta:
        model = ProductMedia
        fields = '__all__'


    '''
    TODO: 
        add perform create to auto set product_id form URL
    '''
        

class CharacteristicSerializer(serializers.ModelSerializer):
    product = ProductNestedSerializer(read_only = True)

    class Meta:
        model = Characteristic
        fields = ['id', 'characteristic', 'descriptions', 'product']

    '''
    TODO: 
        add perform create to auto set product_id form URL
    '''

