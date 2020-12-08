from django.shortcuts import get_object_or_404
from .models import Review, ReviewImage, ReviewRating
from notifications.models import Notification
from rest_framework import generics
from comments.serializers import ReviewSerializer, ReviewImageSerializer, ReviewRatingSerializer

# Create your views here.


class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.filter(reply_to=None).order_by('-created')
    serializer_class = ReviewSerializer


class ReviewRetrieve(generics.RetrieveUpdateAPIView):
    serializer_class = ReviewSerializer

    def get_object(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))


class ReviewImageListCreate(generics.ListCreateAPIView):
    queryset = ReviewImage.objects.all()
    serializer_class = ReviewImageSerializer


class ReviewRatingListCreate(generics.ListCreateAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewRatingSerializer
