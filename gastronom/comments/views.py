from django.shortcuts import get_object_or_404

from rest_framework import generics, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly

from .models import Review, ReviewImage, ReviewRating
from notifications.views import create_notifications
from comments.serializers import ReviewSerializer, ReviewImageSerializer, ReviewRatingSerializer

# Create your views here.


class ReviewListCreate(generics.ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.filter(reply_to=None).order_by('-created')
    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        reply = serializer.data['reply_to']

        if reply:
            review_obj = Review.objects.get(id=reply)
            create_notifications(source='comments.apps.CommentsConfig', recipients=[review_obj.user], send_method='email', subject='Gastronom review', message='You have answer on your review')


class ReviewRetrieve(generics.RetrieveUpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))


class ReviewImageListCreate(generics.ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ReviewImage.objects.all()
    serializer_class = ReviewImageSerializer


class ReviewImageRetrieve(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewImageSerializer
    # permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        return get_object_or_404(ReviewImage, pk=self.kwargs.get('review_id'))


class ReviewRatingListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewRatingSerializer
