from django.contrib.auth.models import User	
from rest_framework import serializers
from .models import Review, ReviewImage, ReviewRating
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


class ReviewImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewImage
        fields = ['review_photo', 'review']



class ReviewRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewRating
        fields = ['liked', 'disliked', 'rating']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    child = RecursiveSerializer(many = True, read_only=True)


    class  Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ['user', 'product', 'text', 'created', 'child']
  