from django.db import models

from catalog.models import Catalog
# TODO add count, price, sku(charfield )
class Product(models.Model):
    product_name = models.CharField(max_length=50, blank=False)
    product_descriptions = models.CharField(max_length=1000)
    product_raiting = models.DecimalField(max_digits=3, decimal_places=1)
    categories = models.ManyToManyField(Catalog)
    
    def __str__(self):
        return self.product_name


class Media(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='mediafiles')
    product_image = models.ImageField(upload_to='../templates/media/%Y/%m/%d/')
    

class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    characteristic = models.CharField(max_length=20)
    descriptions = models.CharField(max_length=500)
    
    def __str__(self):
        return self.characteristic

