from .models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'email', 'gender']
