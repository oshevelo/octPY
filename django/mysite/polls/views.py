from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from rest_framework import generics

from .serializers import QuestionSerializer, ChoiceSerializer
from .models import Question, Choice


# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = 'You`re looking at results of question %s'
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse('You`re voting on question %s.' % question_id)


class ChoiceList(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        return Choice.objects.filter(question_id=self.kwargs.get('question_id'))


class ChoiceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChoiceSerializer

    def get_object(self):
        obj = get_object_or_404(Choice, pk=self.kwargs.get('choice_id'))
        return obj


class QuestionListCreate(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer

    def get_object(self):
        obj = get_object_or_404(Question, pk=self.kwargs.get('question_id'))
        return obj

