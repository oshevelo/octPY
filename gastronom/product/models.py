from django.db import models
from django.utils.text import slugify

from catalog.models import Catalog

import os, datetime


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    descriptions = models.CharField(max_length=1000)
    raiting = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    sku = models.CharField(max_length=10, default='AA22qq55')
    categories = models.ManyToManyField(Catalog)
    
    def __str__(self):
        return self.pk, self.name, self.sku

    def __eq__(self, other):
        return (self.name == other.name) or (self.raiting == other.raiting) or (self.price == other.price)

    def __lt__(self, other):
        return (self.name < other.name) or (self.raiting < other.raiting) or (self.price < other.price)

    def __le__(self, other):
        return (self.name <= other.name) or (self.raiting <= other.raiting) or (self.price <= other.price)



    class Meta:
        ordering = ['name', '-price']


class Media(models.Model):

    UPLOAD_PATH = "../templates/media/"

    def generate_upload_path(self, filename):
        filename, ext = os.path.splitext(filename.lower())
        filename = "%s.%s%s" % (slugify(filename),datetime.datetime.now().strftime("%Y-%m-%d"), ext)
        return '%s/%s' % (UPLOAD_PATH, filename)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='mediafiles')
    product_image = models.ImageField(upload_to=generate_upload_path)


    

class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    characteristic = models.CharField(max_length=20)
    descriptions = models.CharField(max_length=500)
    
    def __str__(self):
        return self.pk, self.product, self.characteristic

