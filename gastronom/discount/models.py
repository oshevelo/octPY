from django.db import models
from datetime import *


class DiscountCart(models.Model):
    cart = models.IntegerField(null=True, blank=True, db_index=True, verbose_name='Cart')
    code = models.CharField(max_length=20, blank=True, null=True, default=None, db_index=True, verbose_name='Promo code')
    valid_date_start = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Active from ')
    valid_date_end = models.DateTimeField(default=datetime.now(timezone.utc) + timedelta(days=90), verbose_name='Active to')
    nominal = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Discount denomination')
    status = models.BooleanField(default=False, verbose_name='Status')

    class Meta:
        verbose_name_plural = 'discounts'
        verbose_name = 'discount'

    def __str__(self):
        return self.code
