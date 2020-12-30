from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrdersList.as_view(), name='list'),
    path('<int:order_id>/', views.OrderDetail.as_view(), name='details'),
]