from django.contrib.auth.models import User	
from rest_framework import serializers
from polls.models import Question


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_desc', 'pub_date']

