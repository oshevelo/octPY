from django.db import models
from django.contrib.postgres.fields import JSONField
from django_fsm import FSMField, transition


class PaymentSystem:
    portmone = 'portmone'
    cash = 'cash'


paymentsystem_list = [
    (PaymentSystem.portmone, 'portmone'),
    (PaymentSystem.cash, 'cash'),
]


class Status:
    submitted = 'submitted'
    processing = 'processing'
    completed = 'completed'
    suspended = 'suspended'
    declined = 'declined'


status_list = [
    (Status.submitted, 'submitted'),
    (Status.processing, 'processing'),
    (Status.completed, 'completed'),
    (Status.suspended, 'suspended'),
    (Status.declined, 'declined'),
]


class Payments(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT,
                             null=True, blank=False
                             )
    order = models.OneToOneField('orders.Order', on_delete=models.PROTECT,
                                 null=True, blank=True
                                 )
    paymentsystem = models.CharField(max_length=10,
                                     choices=paymentsystem_list, default='portmone'
                                     )
    billAmount = models.FloatField(default=0.0)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = FSMField(default=Status.submitted, choices=status_list)

    def permissions(self, user):
        if self.user == user:
            if self.status == Status.submitted:
                return ['can_create', 'can_edit', 'can_delete']
            else:
                return ['can_create']
        else:
            return []

    @transition(field=status, source=['submitted', 'suspended'],
                target='processing'
                )
    def submit(self):
        pass

    @transition(field=status, source='processing', target='suspended')
    def suspend(self):
        pass

    @transition(field=status, source='processing', target='completed')
    def complete(self):
        pass

    @transition(field=status, source=['processing', 'suspended'],
                target='declined'
                )
    def decline(self):
        pass

    @classmethod
    def create_payment(cls, user, order):
        new_payment = cls(user)
        new_payment.order = order
        new_payment.paymentsystem = paymentsystem
        new_payment.billAmount = order.order_cost
        new_payment.save()
        return new_payment

    class Meta:
        verbose_name_plural = 'Payments'

    def __str__(self):
        return 'user {} has payed for order {}'.format(self.user, self.order)


class PaymentSystemLog(models.Model):
    shopOrderNumber = models.ForeignKey('orders.Order',
                                        on_delete=models.PROTECT, null=True, blank=False
                                        )
    payeeId = models.IntegerField(null=True, blank=False)
    dt = models.DateTimeField(auto_now=True)  # sent_at
    billAmount = models.FloatField(null=True, blank=False)
    raw_data = JSONField()

    SHOPBILLID = models.IntegerField(null=True, blank=False)
    SHOPORDERNUMBER = models.CharField(max_length=50, null=True, blank=False)
    BILL_AMOUNT = models.FloatField(null=True, blank=False)
    RESULT = models.SmallIntegerField(null=True, blank=False)
    raw_response = JSONField()

    def __str__(self):
        return 'order {} is prossed {}'.format(self.order, self.processed_ok)