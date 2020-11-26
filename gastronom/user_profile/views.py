from django.shortcuts import render
from django.http import HttpResponse
from .serializers import UserProfileSerializer
from .models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import filters
from django.urls import reverse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
    

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    search_fields = ['first_name', 'last_name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = UserProfileSerializer

    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])
        
        
class UserProfileDetails(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return get_object_or_404(UserProfile, pk=self.kwargs.get('user_id'))
