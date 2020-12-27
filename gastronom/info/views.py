from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from info.models import InfoPost
from rest_framework.pagination import LimitOffsetPagination

from rest_framework import generics
from info.serializers import InfoPostSerializer, InfoPostDetailSerializer
from django.shortcuts import get_object_or_404
from django.shortcuts import render


class InfoPostList(generics.ListCreateAPIView):
    queryset = InfoPost.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = InfoPostSerializer


class InfoPostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InfoPostDetailSerializer

    def get_object(self):
        return get_object_or_404(InfoPost, pk=self.kwargs.get('infopost_index'))
