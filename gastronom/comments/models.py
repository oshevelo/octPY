from django.db import models
from django.contrib.auth.models import User
# from product.model import Product
# Create your models here.


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='review_user')
    text = models.TextField(max_length=5000)
    # product = models.ForeignKey(Product, verbose_name='rewiew_product', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    useful = models.SmallIntegerField(default=0)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='reply_review', null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Review by {self.user} on {self.product}'


class CommentGalleryItem(models.Model):
    review_photo = models.ImageField(upload_to='reviews/', null=True, blank=True)
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE)


class UsefulKarma(models.Model):
    reviews = models.ManyToManyField(Reviews)
