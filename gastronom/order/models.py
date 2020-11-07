from django.db import models
import datetime
from django.utils import timezone



# Create your models here.

class Order(models.Model):
    delivery_methods = (
    [pickup, 'Самовывоз'],
    [kiev_delivery, 'Доставка по Киеву'],
    [ukraine_deivery, 'Доставка по Украине']
    )
    payment_methods = (
    [prepayment, 'Предоплата картой'],
    [postpayment, 'Оплата при получении']
    )
    date=models.DateTimeField('date published')
    number=models.IntegerField(default=0)
    user=models.ForeignKey(User, on_delete=models.SET_NULL)
    delivery_method=models.IntegerField(choices=delivery_methods, default=pickup)
    payment_method=models.IntegerField(choices=payment_methods, default=prepayment)
    cart=models.ForeignKey(Cart, on_delete=models.SET_NULL)




class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL)
    count=models.IntegerField(default=0)
    final_price=models.FloatField(default=0)