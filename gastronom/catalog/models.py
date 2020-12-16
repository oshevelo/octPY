from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Catalog(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    index = models.IntegerField(default=1)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

# class Catalog(MPTTModel):
#     name = models.CharField(max_length=50)
#     description = models.TextField(null=True, blank=True)
#     index = models.IntegerField(default=1)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
#
#     def __str__(self):
#         return self.name
#
#     class MPTTMeta:
#         order_insertion_by = ['name']
#
#
# class Genre(MPTTModel):
#     name = models.CharField(max_length=50, unique=True)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
#
#     def __str__(self):
#         return self.name
#
#     class MPTTMeta:
#         order_insertion_by = ['name']
'''
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
'''

