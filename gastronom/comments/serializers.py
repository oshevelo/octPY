from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Review, ReviewImage, ReviewRating


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializers = self.parent.parent.__class__(value, context=self.context)
        return serializers.data


class ReviewImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewImage
        fields = ['review_photo', 'raw_photo', 'review']
        read_only_fields = ['review_photo']


class ReviewRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewRating
        fields = ['review_reting', 'negative_rating', 'positive_rating']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    child = RecursiveSerializer(many=True, read_only=True)

    class Meta:
    
        model = Review
        fields = ['user', 'product', 'text', 'created', 'child', 'reply_to']
