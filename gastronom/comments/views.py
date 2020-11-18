from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Review, GalleryImageReview, ReviewRating
from notifications.models import Notification
from rest_framework import generics
from comments.serializers import ReviewSerializer, GalleryImageSerializer, ReviewRatingSerializer

# Create your views here.


class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all().order_by('-created')
    serializer_class = ReviewSerializer



class ReviewRetrieve(generics.RetrieveUpdateAPIView):
    serializer_class = ReviewSerializer

    def get_object(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))



class GalleryImageListCreate(generics.ListCreateAPIView):
    queryset = GalleryImageReview.objects.all()
    serializer_class = GalleryImageSerializer


class ReviewLikeListCreate(generics.ListCreateAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewRatingSerializer
