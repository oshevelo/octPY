from django.urls import path
from django_filters.views import FilterView

from notifications import views
from notifications.filters import NotificationFilter


urlpatterns = [
    path('last/', views.NotificationListCreate().as_view(), name='last_created_notifications'),
    path('recipient/<int:recipient_id>/', views.NotificationsByRecipient().as_view(),
         name='notifications_by_recipient'),
    path('recipient/<int:recipient_id>/nested/', views.NotificationsByUserNested().as_view(),
         name='notifications_by_recipient_nested'),
    path('unsent/', views.NotificationsUnsent().as_view(),
         name='notifications_unsent_by_recipient_nested'),
    path('', FilterView.as_view(filterset_class=NotificationFilter)),
    path('all/', views.NotificationAll.as_view(), name='notifications_with_filtration')
]
