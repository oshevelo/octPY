from rest_framework import serializers
from .models import Choice, Question


class ChoiceNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['id', 'question_id', 'choice_text']


class QuestionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text']


class ChoiceSerializer(serializers.ModelSerializer):
    question = QuestionNestedSerializer(read_only=True)

    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes', 'question']


class QuestionSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    choices = ChoiceNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'author', 'choices']
