from django.urls import path

from . import views

urlpatterns = [
    path('api/products', views.ProductList, name='api_products_list'),
    path('api/products/<int product_id:', views.ProductDetail, name='api_product_detail'),
    path('api/products/<int product_id:/media', views.MediaList, name='api_product_media'),
    path('api/products/<int product_id:/characteristics', views.CharacteristicList, name='api_product_characteristics'),
    ]
