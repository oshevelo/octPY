from django.db import models
import datetime
from django.utils import timezone



# Create your models here.

class Order(models.Model):
    delmet = (
    [1, 'Самовывоз']
    , [2, 'Доставка по Киеву']
    , [3, 'Доставка по Украине']
    )
    paymet = (
    [1, 'Предоплата картой']
    , [2, 'Оплата при получении']
    )
    orderdate=models.DateTimeField('date published')
    ordernum=models.IntegerField(default=0)
    orderuser=models.ForeignKey(User, on_delete=models.CASCADE)
    orderdelmet=models.IntegerField(choices=delmet, default=1)
    orderdeldate=models.DateTimeField(default=)
    orderpaymet=models.IntegerField(choices=paymet, default=1)




class OrderItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)