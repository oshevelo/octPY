from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from gastronom.settings import REVIEW_IMAGE_SIZE, USE_QUEUE
from product.models import Product
from comments.tasks import resize

from PIL import Image
from io import BytesIO
# Create your models here.


def review_photo_path(instance, filename):
    review_photo_name = f'review_{instance.review.id}/{instance.raw_photo}'  # make a folder for images in reviews
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
    raw_photo = models.ImageField(upload_to=review_photo_path, null=True, blank=True)

    def __str__(self):
        return f'Image for {self.review}'

    def save(self, **kwargs):
        raw_photo_path = ReviewImage.raw_photo.path
        
        self.review_photo.save(
            **self.resize_img(REVIEW_IMAGE_SIZE, raw_photo_path)
        )

        super().save(**kwargs)

    def resize_img(self, REVIEW_IMAGE_SIZE, raw_photo_path):

        if USE_QUEUE:
            resize.delay(REVIEW_IMAGE_SIZE, raw_photo_path)
        else:
            resize(REVIEW_IMAGE_SIZE, raw_photo_path)


class ReviewRating(models.Model):
    review_reting = models.ManyToManyField(Review, related_name='review_rating', blank=True)
    negative_rating = models.IntegerField(default=0, blank=True)
    positive_rating = models.IntegerField(default=0, blank=True)
