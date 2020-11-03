from django.contrib.auth.models import User	
from rest_framework import serializers
from .models import Question, Choice


class ChoiceNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['id', 'choice_text']


class QuestionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'question_votes', 'choices']


class ChoiceSerializer(serializers.ModelSerializer):
    question = QuestionNestedSerializer(read_only=True)

    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes', 'question']
