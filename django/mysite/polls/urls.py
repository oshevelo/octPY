from django.urls import path
from . import views


app_name = "polls"
urlpatterns = [
    path('', views.index, name='index'),
    path('question/', views.QuestionListCreate.as_view(), name='question_list'),
    path('question/<int:question_id>', views.QuestionDetail.as_view(), name='question_detail'),
    path('question/<int:question_id>/choice/', views.ChoiceList.as_view(), name='list'),
    path('choice/<int:choice_id>', views.ChoiceDetail.as_view(), name='choice_detail')
]