from django.contrib.auth.models import User	
from rest_framework import serializers
from .models import Review, GalleryImageReview, ReviewRating
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
     
     class Meta:
         model = User
         fields = ['username']


class FilterReviewListSerializer(serializers.ListSerializer):
    
    def to_representation(self, data):
        data = data.filter(reply_to=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializers = self.parent.parent.__class__(value, context = self.context)
        return serializers.data


class GalleryImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GalleryImageReview
        fields = ['review', 'review_photo']


class ReviewRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewRating
        fields = ['liked', 'disliked', 'rating']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    child = RecursiveSerializer(many = True)

    class  Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ['user', 'text', 'created', 'child']
