from django.db import models
from django.utils.text import slugify
from django.core.files.uploadedfile import InMemoryUploadedFile

from catalog.models import Catalog
from gastronom.settings import PRODUCT_IMAGE_SIZE

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    descriptions = models.TextField(max_length=1000)
    raiting = models.FloatField(default=0.0)
    count = models.IntegerField(blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)
    sku = models.CharField(max_length=10, blank=True, unique=True)
    categories = models.ManyToManyField(Catalog)
    available = models.BooleanField(default=True, verbose_name="Available")
    
    def __str__(self):
        return f"{self.pk}, {self.name}, {self.sku}"

    class Meta:
        ordering = ['name', '-price']


class ProductMedia(models.Model):

    medium_size = PRODUCT_IMAGE_SIZE['medium']
    thumbnail_size = PRODUCT_IMAGE_SIZE['thumbnail']

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='mediafiles')
    image = models.ImageField(upload_to='products/%Y/%m/%d/original/', null=True)

    thumbnail_image = ImageSpecField(
                source='image',
                cachefile_storage='products/%Y/%m/%d/thumbnail/',
                processors=[ResizeToFill(width=thumbnail_size[0], height=thumbnail_size[1])],
                options={'quality': 60})

    medium_image = ImageSpecField(
                source='image',
                cachefile_storage='products/%Y/%m/%d/medium/',
                processors=[ResizeToFill(width=medium_size[0], height=medium_size[1])],
                options={'quality': 60})



class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    characteristic = models.CharField(max_length=20)
    descriptions = models.TextField(max_length=500)
    
    def __str__(self):
        return f"{self.pk}, {self.product}, {self.characteristic}"

    class Meta:
        ordering = ['product_id']

