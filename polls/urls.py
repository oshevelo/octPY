from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('api/question/', views.QuestionList.as_view(), name='api_question_list'),
    path('api/question/<int:question_id>', views.QuestionDetail.as_view(), name='api_question_details'),
    path('api/question/<int:question_id>/choice/', views.ChoiceList.as_view(), name='api_choice_list'),
    path('api/question/<int:question_id>/choice/<int:choice_id>', views.ChoiceDetail.as_view(), name='api_choice_details'),
]
