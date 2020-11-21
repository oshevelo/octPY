from django.urls import path

from . import views

urlpatterns = [
    path('', views.CartList.as_view(), name='cart_list'),
    path('cart_item/', views.CartDetail.as_view(), name='cart_detail'),
    path('cart_item/<int:cart_item_id>/', views.CartItemDetail.as_view(), name='cart_item_detail'),
]
