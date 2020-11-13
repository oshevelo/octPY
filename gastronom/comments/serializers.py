from django.contrib.auth.models import User	
from rest_framework import serializers
from .models import Review, GalleryImageReview, ReviewLike


class ReviewSerializer(serializers.ModelSerializer):
    
    class  Meta:
        model = Review
        fields = ['user', 'text', 'created', 'reply_to']


class GalleryImageSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True, read_only=True)


    class Meta:
        model = GalleryImageReview
        fields = ['review_photo', 'review']


class ReviewLikeSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True, read_only=True)


    class Meta:
        model = ReviewLike
        fields = ['like', 'reviews']