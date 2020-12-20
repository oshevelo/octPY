from django.urls import path

from . import views

urlpatterns = [
    path('info/', views.InfoPostList.as_view(), name='list'),
    path('info/<int:infopost_id>/', views.InfoPostDetail.as_view(), name='details'),
]