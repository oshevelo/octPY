from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='products_list'),
    path('<int:product_id>/', views.ProductDetail.as_view(), name='products_detail'),
    path('<int:product_id>/media/', views.ProductMediaList.as_view(), name='product_media'),
    path('<int:product_id>/media/<int:productmedia_id>/', views.ProductMediaDetail.as_view(), name='product_media_detail'),
    path('<int:product_id>/characteristics/', views.CharacteristicList.as_view(), name='product_characteristics'),
    path('<int:product_id>/characteristics/<int:characteristic_id>/', views.CharacteristicDetail.as_view(), name='product_characteristics_detail'),
    ]
