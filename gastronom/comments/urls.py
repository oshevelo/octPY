from django.urls import path

from . import views

urlpatterns = [
    
    path('reviews/', views.ReviewListCreate.as_view(), name='review_list'),

]
    
