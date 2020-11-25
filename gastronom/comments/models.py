from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from PIL import Image
# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    text = models.TextField(max_length=5000)
    product = models.ForeignKey(Product, verbose_name='rewiew_product', on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='child', null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Review by {self.user} on {self.product}'


class ReviewImage(models.Model):
    review_photo = models.ImageField(upload_to='reviews/', null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)


    def __str__(self):
        return f'Image for {self.review}'



class ReviewRating(models.Model):
    liked_review = models.ManyToManyField(Review, related_name='liked_review', blank=True)
    disliked_review = models.ManyToManyField(Review, related_name='disliked_review', blank=True)
    rating = models.IntegerField(default=0, blank=True)
