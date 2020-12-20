from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Review, ReviewImage, ReviewRating
from notifications.views import create_notifications
from comments.serializers import ReviewSerializer, ReviewImageSerializer, ReviewRatingSerializer

# Create your views here.


class ReviewListCreate(generics.ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    permission_class = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.filter(reply_to=None).order_by('-created')
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        reply = serializer.data['reply_to']
    
        if reply:
            user_obj = Review.objects.select_related('user').filter(id=reply)
            print(user_obj)
            # pamagite!
            # create_notifications(source='comments.apps.CommentsConfig', recipients=reply_to, send_method='email', subject='You have answer')



class ReviewRetrieve(generics.RetrieveUpdateAPIView):
    serializer_class = ReviewSerializer
    permission_class = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))


class ReviewImageListCreate(generics.ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    queryset = ReviewImage.objects.all()
    serializer_class = ReviewImageSerializer


class ReviewImageRetrieve(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewImageSerializer
    permission_class = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(ReviewImage, pk=self.kwargs.get('review_id'))


class ReviewRatingListCreate(generics.ListCreateAPIView):
    permission_class = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewRatingSerializer
