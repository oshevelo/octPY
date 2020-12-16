from django.db import models

class Payment(models.Model):
    payment_id = models.CharField('payment_id', max_length=50, primary_key=True, null=False)
    order_id = models.CharField('order_id', max_length=50, primary_key=False, null=False)
    payment_system = models.CharField('payment_system', max_length=100, primary_key=False, null=False)
    total_amount = models.IntegerField('total_amount', primary_key=False, null=False)


def __str__(self):
    return self.payment_id
