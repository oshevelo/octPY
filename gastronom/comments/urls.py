from django.urls import path

from . import views

urlpatterns = [
    
    path('reviews/', views.ReviewListCreate.as_view(), name='review_list'),
    path('reviews/<int:review_id>/', views.ReviewRetrieve.as_view(), name='review_details'),
    path('reviews-image/', views.GalleryImageListCreate.as_view(), name='image_list'),
    path('review-likes/', views.ReviewLikeListCreate.as_view(), name='like_list'),

]
    
