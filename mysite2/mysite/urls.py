#from rest_framework import routers, serializers, viewsets
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
