from django.db import models


class Catalog(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    index = models.IntegerField()
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


'''
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
'''

