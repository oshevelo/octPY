from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('other/', views.index_other, name='index'),
    path('question/', views.QuestionList.as_view(), name='list'),
    path('question/<int:question_id>/', views.QuestionDetail.as_view(), name='details'),
    path('question/<int:question_id>/choise/', views.ChoiceList.as_view(), name='choice-list'),
    path('choice/', views.ChoiceList.as_view(), name='list'),
    path('choice/<int:choice_id>/', views.ChoiceDetail.as_view(), name='details'),
]
