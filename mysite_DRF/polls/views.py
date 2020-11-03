
from django.http import HttpResponse
from polls.models import Question, Choice

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from polls.serializers import QuestionSerializer, ChoiceSerializer
from django.shortcuts import get_object_or_404


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer

    def get_object(self):
        return get_object_or_404(Question, pk=self.kwargs.get('question_id'))


class ChoiceList(APIView):
    def get(self, request):
        choice = Choice.objects.all()
        serializer = ChoiceSerializer(choice, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChoiceDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ChoiceSerializer

    def get_object(self):
        return get_object_or_404(Choice, pk=self.kwargs.get('choice_id'))
