# from django.db import models
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField(blank=True)
#
#     def __str__(self):
#         return self.name

#
# class Subcategory(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     category = models.ForeignKey(Category.name, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name