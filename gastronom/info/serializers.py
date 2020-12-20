from django.contrib.auth.models import User
from rest_framework import serializers
from info.models import InfoPost


class InfoPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfoPost
        fields = ['title', 'content', 'index']


class InfoPostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfoPost
        fields = '__all__'
