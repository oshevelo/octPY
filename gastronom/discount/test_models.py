from datetime import *

from django.test import TestCase
from discount.models import DiscountCart



def compute_default_to():
    return datetime.now() + timedelta(days=20)





class DiscountCartModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        DiscountCart.objects.create(
            code='111',
            valid_date_start=datetime.now(),
            valid_date_end=datetime.now(),
            nominal=1000.00,
            status=True
        )

    # Тесты лэйблов полей в моделе.
    def test_code_label(self):
        discount = DiscountCart.objects.get(id=1)
        field_label = discount._meta.get_field('code').verbose_name

        self.assertEquals(field_label, 'Промо код')

    def test_valid_date_start_label(self):
        discount = DiscountCart.objects.get(id=1)
        field_label = discount._meta.get_field('valid_date_start').verbose_name

        self.assertEquals(field_label, 'Начало действия')

    def test_valid_date_end_label(self):
        discount = DiscountCart.objects.get(id=1)
        field_label = discount._meta.get_field('valid_date_end').verbose_name

        self.assertEquals(field_label, 'Конец действия')

    def test_nominal_label(self):
        discount = DiscountCart.objects.get(id=1)
        field_label = discount._meta.get_field('nominal').verbose_name

        self.assertEquals(field_label, 'Номинал скидки')

    def test_status_label(self):
        discount = DiscountCart.objects.get(id=1)
        field_label = discount._meta.get_field('status').verbose_name

        self.assertEquals(field_label, 'Статус')

    # Проверка длины полей в моделе.
    def test_code_max_length(self):
        discount = DiscountCart.objects.get(id=1)
        max_length = discount._meta.get_field('code').max_length
        self.assertEquals(max_length, 20)

    def test_nominal_max_digits(self):
        discount = DiscountCart.objects.get(id=1)
        max_length = discount._meta.get_field('nominal').max_digits
        self.assertEquals(max_length, 10)

    # Проверка, что отдает объект модели
    def test_object_name_is_code_name(self):
        discount = DiscountCart.objects.get(id=1)
        expected_object_name = '%s' % discount.code
        self.assertEquals(expected_object_name, str(discount))
