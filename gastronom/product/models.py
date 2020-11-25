from django.db import models
from django.utils.text import slugify
from django.core.files.uploadedfile import InMemoryUploadedFile

from catalog.models import Catalog

from io import BytesIO
import os
from datetime import datetime
from PIL import Image


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    descriptions = models.CharField(max_length=1000)
    raiting = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    sku = models.CharField(max_length=10, default='AA22qq55')
    categories = models.ManyToManyField(Catalog)
    available = models.BooleanField(default=True, verbose_name="Available")
    
    def __str__(self):
        return f"{self.pk}, {self.name}, {self.sku}"

    @property
    def amount_left(self):
        if self.count <= 0:
            self.available = False
            self.save()
            return 0
        else:
            self.available = True
            self.save()
            return self.count


    class Meta:
        ordering = ['name', '-price']


class Media(models.Model):
    #filename = str(datetime.now().strftime("%Y-%m-%d"))
    #upload_path = "products/" + filename
    
    def generate_upload_path(self, filename):
        dir_name = str(datetime.now().strftime("%Y-%m-%d"))
        UPLOAD_PATH = f"products/{dir_name}"
        filename, ext = os.path.splitext(filename.lower())
        filename = "%s.%s%s" % (slugify(filename),datetime.now().strftime("%Y-%m-%d"), ext)
        return '%s/%s' % (UPLOAD_PATH, filename)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='mediafiles')
    product_image = models.ImageField(upload_to=generate_upload_path, null=True)

    
    def create_thumbnail(self):
        image = Image.open(self.product_image.file.file)
        image.thumbnail(size=(100, 100))
        image_file = BytesIO()
        image.save(image_file, image.format)
        self.thumbnail_image.save(
            self.image.name,
            InMemoryUploadedFile(
                image_file,
                None, '',
                self.image.file.content_type,
                image.size,
                self.image.file.charset,
            ),
            save=False
        )

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.product_image.path)

        if img.height > 100 or img.weight > 100:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(self.product_image.path)

    class Meta:
        ordering = ['product_id']

    

class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    characteristic = models.CharField(max_length=20)
    descriptions = models.CharField(max_length=500)
    
    def __str__(self):
        return f"{self.pk}, {self.product}, {self.characteristic}"

    class Meta:
        ordering = ['product_id']

