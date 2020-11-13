from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Review, GalleryImageReview, ReviewLike
from notifications.models import Notification
from rest_framework import generics
from comments.serializers import ReviewSerializer, GalleryImageSerializer, ReviewLikeSerializer

# Create your views here.


class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    
'''
    def perform_create(self, serializer):
        serializer.save()
        if :
            reply_notification = Notification(self)
            reply_notification.create_notifications('comments.apps.CommentsConfig', self.request.user, 'You have an answer', 'email')
'''
