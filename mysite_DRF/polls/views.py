from django.http import HttpResponse
from .models import Question, Choice

from rest_framework import generics
from .serializers import QuestionSerializer
from .serializers import ChoiceSerializer
from django.shortcuts import get_object_or_404


def index(request):
    question_list = Question.objects.all()
    return HttpResponse(', '.join([q.question_text for q in question_list]))


def index_other(request):
    return HttpResponse("Hello, OTHER world. You're at the polls index.")


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer

    def get_object(self):
        return get_object_or_404(Question, pk=self.kwargs.get('question_id'))


class ChoiceList(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class ChoiceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChoiceSerializer

    def get_object(self):
        return get_object_or_404(Choice, pk=self.kwargs.get('choice_id'))
