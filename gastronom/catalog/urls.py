from django.urls import path

from . import views

urlpatterns = [
    path('catalog/', views.CatalogList.as_view(), name='list'),
    path('catalog_tree/', views.CatalogTree.as_view(), name='list'),
    path('catalog/<int:catalog_id>/', views.CatalogDetail.as_view(), name='details'),
]