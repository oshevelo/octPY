from django.contrib.auth.models import User	
from rest_framework import serializers
from polls.models import Question, Choice


class ChoiceNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['id', 'choice_text']


class QuestionSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField(required=False)
    choices = ChoiceNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'question_votes', 'choices']


class QuestionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text']


class ChoiceSerializer(serializers.ModelSerializer):
    question = QuestionNestedSerializer(read_only=True)
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes', 'question']
