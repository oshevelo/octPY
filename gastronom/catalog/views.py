from django.http import HttpResponse
from django.http import Http404
from catalog.models import Catalog

from rest_framework import generics
from catalog.serializers import CatalogSerializer
from django.shortcuts import get_object_or_404
from django.shortcuts import render


class CatalogList(generics.ListCreateAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


