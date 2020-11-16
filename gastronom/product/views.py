from django.shortcuts import render

from rest_framework import generics

from product.models import Product, Media, Characteristic
from product.serializers import ProductSerializer, MediaSerializer, CharacteristicSerializer

