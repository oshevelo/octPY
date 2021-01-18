from django.http import HttpResponse
from django.http import Http404
from catalog.models import Catalog

from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from catalog.serializers import CatalogSerializer, CatalogDetailedSerializer, CatalogTreeSr
from django.shortcuts import get_object_or_404
from django.shortcuts import render


class CatalogList(generics.ListCreateAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]


class CatalogDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CatalogDetailedSerializer

    def get_object(self):
        return get_object_or_404(Catalog, pk=self.kwargs.get('catalog_id'))


class CatalogTree(generics.ListAPIView):
    serializer_class = CatalogTreeSr
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Catalog.objects.exclude(parent__isnull=False)

