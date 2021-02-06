from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Payment
from datetime import date


class PaymentsTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        self.user = User.objects.create()
        self.payment = Payment.objects.create(
            payment_id=3333,
            order_id=1111,
            payment_system='portmone',
            payment_amount=500.0,
            user_id=self.user_id,
            payment_date=date.today(),
            paymetn_status='completed',

        )
        self.client = APIClient()
