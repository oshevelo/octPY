from django.urls import include, path
from . import views


urlpatterns = [
    path('user_profile/', views.UserProfileList.as_view(), name='list'),
    path('user_profile/<int:user_id>/', views.UserProfileDetails.as_view(), name='details'),
]
