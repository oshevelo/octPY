from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    category_description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.category_name

'''
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.ManyToManyField(Category)
'''

