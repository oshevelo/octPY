from django.urls import path

from notifications import views


urlpatterns = [
    path('last/', views.NotificationListCreate().as_view(), name='last_created_notifications'),
    path('recipient/<int:recipient_id>/', views.NotificationsByRecipient().as_view(),
         name='notifications_by_recipient'),
    path('recipient/<int:recipient_id>/nested/', views.QuestionChoiceNested().as_view(),
         name='notifications_by_recipient_nested'),
]
