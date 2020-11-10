from django.db import models
from django.contrib.auth.models import User

# from gastronom.product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Owner')
    creation_date = models.DateTimeField('Creation date', auto_now_add=True)

    def __str__(self):
        return f'User = {self.user}; pk = {self.pk}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Cart')
    # product = models.ForeignKey(Product, verbose_name='Product')
    quantity = models.PositiveIntegerField('Quantity', default=1, null=True, blank=True)
    price = models.DecimalField('Price', max_digits=15, decimal_places=2)
    creation_date = models.DateTimeField('Creation date', auto_now_add=True)
