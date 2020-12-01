from django.db import models
from django.contrib.auth.models import User
from gastronom.settings import REVIEW_IMAGE_SIZE
from product.models import Product
from PIL import Image
# Create your models here.


def review_photo_path(instance, filename):
    review_photo_name = f'review_{instance.review.id}/{instance.review_photo}'  # make a folder for images in reviews
    return review_photo_name


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
    review_photo = models.ImageField(upload_to=review_photo_path, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return f'Image for {self.review}'

    def save(self, *args, **kwargs): 
        '''
        Saving the picture in a scale for easy display in reviews 300x300
        '''
        super().save(*args, **kwargs)

        if self.review_photo:
            img = Image.open(self.review_photo.path)
            img.thumbnail(REVIEW_IMAGE_SIZE, Image.LANCZOS)
            img.save(self.review_photo.path)


class ReviewRating(models.Model):
    liked_review = models.ManyToManyField(Review, related_name='liked_review', blank=True)
    disliked_review = models.ManyToManyField(Review, related_name='disliked_review', blank=True)
    rating = models.IntegerField(default=0, blank=True)
