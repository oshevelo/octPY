from django.urls import path

from . import views

urlpatterns = [
    path('api/products/', views.ProductList.as_view(), name='products-list'),
    path('api/products/<int:product_id>/', views.ProductDetail.as_view(), name='products-detail'),
    path('api/products/<int:product_id>/media/', views.ProductMediaList.as_view(), name='product-media'),
    path('api/products/<int:product_id>/characteristics/', views.CharacteristicList.as_view(), name='product-characteristics'),
    ]
