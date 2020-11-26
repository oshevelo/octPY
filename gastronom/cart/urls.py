from django.urls import path

from . import views


urlpatterns = [
    path('', views.CartList.as_view(), name='CartList'),
    path('<int:cart_id>/', views.CartDetail.as_view(), name='CartDetail'),
    path('<int:cart_id>/cart_item/', views.CartItemList.as_view(), name='CartItemList'),
    path('<int:cart_id>/cart_item/<int:cart_item_id>/', views.CartItemDetail.as_view(), name='CartItemDetail'),
]
