from django.db import models
from django.utils.text import slugify
from django.core.files.base import ContentFile

from catalog.models import Catalog
from gastronom.settings import PRODUCT_IMAGE_SIZE

from datetime import datetime
from PIL import Image
from io import BytesIO
import os


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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='mediafiles')
    original_image = models.ImageField(upload_to='products/%Y/%m/%d/original/', null=True)
    thumbnail_image = models.ImageField(upload_to='products/%Y/%m/%d/thumbnails/', null=True, editable=False)


    def save(self):
        for sizes in PRODUCT_IMAGE_SIZE.values():

            if not self.make_thumbnail(sizes):

                raise Exception('Could not create thumbnail - is the file type valid?')
        
        super(ProductMedia, self).save()

    def make_thumbnail(self, sizes):
        image = Image.open(self.original_image)
        image.thumbnail(sizes, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.original_image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail_image.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True



class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    characteristic = models.CharField(max_length=20)
    descriptions = models.TextField(max_length=500)
    
    def __str__(self):
        return f"{self.pk}, {self.product}, {self.characteristic}"

    class Meta:
        ordering = ['product_id']

