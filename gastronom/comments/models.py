from django.db import models
from product.model import Product
# Create your models here.


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    review_photo = models.ImageField(upload_to='reviews/')
    text = models.TextField(max_length=500)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    useful = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Review by {self.name} on {self.product}'


class NestedReviews(models.Model):
    nested_review = models.ForeignKey(Reviews, verbose_name='Reviews on review', on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField()
    name = models.CharField(max_length=50)
    review_photo = models.ImageField(upload_to='reviews/')
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    useful = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Review by {self.name} on {self.nested_review}'
