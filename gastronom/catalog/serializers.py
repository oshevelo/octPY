from django.contrib.auth.models import User
from rest_framework import serializers
from catalog.models import Catalog


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = ['name']


class CatalogDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = '__all__'

