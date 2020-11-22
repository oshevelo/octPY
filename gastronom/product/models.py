from django.db import models

from catalog.models import Catalog

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


class Media(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='mediafiles')
    product_image = models.ImageField(upload_to='../templates/media/%Y/%m/%d/')
    

class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    characteristic = models.CharField(max_length=20)
    descriptions = models.CharField(max_length=500)
    
    def __str__(self):
        return self.pk, self.product, self.characteristic

