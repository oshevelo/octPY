from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Payments
from datetime import date


class PaymentsTestCase(TestCase):

    maxDiff = None

    def setUp(self):
        self.user = User.objects.create()
        self.payment = Payments.objects.create(
            user = self.user,
            order = self.order,
            paymentsystem = 'portmone',
            billAmount = 100.0,
            payment_date = date.today(),
            status = 'completed',
        )
        self.client = APIClient()


    def test_payments_get(self):
        print()
        response = self.client.get('/payments/')
        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertEqual(response.json(),{
            'count': 1,
            'next': None,
            'previous': None,
            'results': [{
                'id': self.payment.id,
                'user': self.user.id,
                'order':{
                    # 'id': self.payment.id,
                    'user': self.user.id,
                    'order_status': self.order.order_status,
                    'order_payment': self.order.order_payment,
                },
                'paymentsystem': str(self.payment.paymentsystem),
                'billAmount': self.payment.billAmount,
                'payment_date': str(
                    self.payment.payment_date.isoformat().replace('+00:00','Z')
                ),
                'status': str(self.payment.status),
                'permissions': self.payment.permissions(user=self.user.id),
            }]
        })
#TODO
    def test_payments_post(self):
        number =  self.payment.id
        request = self.client.post('/payments/',{
            'user': self.user.id,
            'id': self.payment.id,
            'payment_date': date.today(),
            'user': self.user.id,
            'order': {
                'user': self.user.id,
                'order_status': self.order.order_status,
                'order_payment': self.order.order_payment,
            },
            'paymentsystem': self.payment.paymentsystem,
            'billAmount': self.payment.billAmount,
            'status': self.payment.status,
        })
        print(request.json())

        self.assertEqual(request.status_code, 201)