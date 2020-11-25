"""
loggers URL Configuration
"""
from django.contrib import admin
from django.urls import path
from notifications.views import index


urlpatterns = [
    path('', index, name='loggers index')
]
