from django.db import models


class Payment(models.Model): payment_id = models.CharField('payment_id', max_length=50, primary_key=True, null=False)


order_id = models.CharField('order_id', max_length=50, primary_key=False, null=False)
payment_system = models.CharField('payment_system', max_length=100, primary_key=False, null=False)
payment_amount = models.IntegerField('payment_amount', primary_key=False, null=False)
user_id = models.CharField('user_id', max_length=50, primary_key=False, null=False)
payment_date = models.DateTimeField('payment_date', primary_key=False, null=False)
paymetn_status = models.CharField('paymetn_status', max_length=50, primary_key=False, null=False)


def __str__(self):
    return self.title

    # Change name of table


class Meta:
    verbose_name = 'Specific task'
    verbose_name_plural = 'All tasks'
