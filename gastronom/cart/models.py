from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Owner')
    creation_date = models.DateTimeField('Creation date', auto_now_add=True)

    def total_price(self):
        return sum([cartitem.product.price * cartitem.quantity for cartitem in self.cart_items.all()
                    if cartitem.cart_item_status == 'Available'])
    total_price = property(total_price)

    def __str__(self):
        return f'User = {self.user}; pk = {self.pk}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Cart', related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Product')
    quantity = models.PositiveIntegerField('Quantity', default=1)
    unit_price = models.DecimalField('Price', max_digits=15, decimal_places=2)
    creation_date = models.DateTimeField('Creation date', auto_now_add=True)

    def amount_left(self):
        return self.product.amount_left
    stock_count = property(amount_left)

    def cart_item_status(self):
        if self.product.available is True and self.quantity <= self.product.amount_left:
            return 'Available'
        elif self.product.available is True and self.quantity > self.product.amount_left:
            return 'An insufficient amount'
        else:
            return 'Not available'
    cart_item_status = property(cart_item_status)
