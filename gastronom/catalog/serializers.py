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


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CatalogTreeSr(serializers.ModelSerializer):
    children = RecursiveField(many=True, allow_null=True)

    class Meta():
        model = Catalog
        fields = ['name', 'description', 'index', 'children']
