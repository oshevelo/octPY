from django.shortcuts import render
from notifications.models import Notification
from django.http import HttpResponse
from django.urls import reverse


def index(request):
    notification_list = Notification.objects.all()
    return HttpResponse('http://127.0.0.1:8000' + reverse('list'))
