from django.db import models
from datetime import datetime

from user_profile.models import UserProfile
from product.models import Product


class Order(models.Model):
    ORDERS_STATUS = [
        ('Processed', 'Processed'),
        ('On_the_road', 'On the road'),
        ('Ready_for_delivery', 'Ready for delivery'),
        ('Received_by_the_customer', 'Received by the customer')
    ]
    SHIPMENT = [
        ('Courier_delivery', 'Courier delivery'),
        ('Mail_delivery', 'Mail delivery'),
        ('Pickup', 'Pickup')
    ]
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    orders_timedate = models.DateTimeField(default=datetime.now)
    content = models.ManyToManyField(Product)
    orders_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipment_type = models.CharField(max_length=20, choices=SHIPMENT, default='Pickup')
    status = models.CharField(max_length=20, choices=ORDERS_STATUS, default='Processed')
    is_it_active = models.BooleanField(default=True, verbose_name='Active?')

    def __str__(self):
        return f' {self.customer}, {self.orders_timedate}, {self.content}, {self.orders_price}, {self.shipment_type},' \
               f' {self.status}, {self.is_it_active} '
