from datetime import *
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from discount.models import DiscountCart






def compute_default_to():
    return datetime.now() + timedelta(days=20)




class DiscountCartViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создадим 3 скидочных промокода"""
        number_of_discount_codes = 3
        for discount_code_num in range(number_of_discount_codes):
            DiscountCart.objects.create(
                code='111%s' % discount_code_num,
                valid_date_start=datetime.now(),
                valid_date_end=datetime.now(),
                nominal=1000.00 + int(discount_code_num),
                status=True
            )

    def setUp(self):
        # Создание токена для общения с сервисом.
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

        # Создание данных для post-запросов в сервис.
        self.url = '/api/v1/discount'

        self.data_for_positive_amount = {"cart": 111, "code": '1111', "amount_cart": 1002.00}
        self.response_for_positive_amount = self.client.post(
            self.url,
            self.data_for_positive_amount,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        self.data_for_negative_amount = {"cart": 112, "code": '1112', "amount_cart": 1000.00}
        self.response_for_negative_amount = self.client.post(
            self.url,
            self.data_for_negative_amount,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

    @staticmethod
    def setup_user():
        user = get_user_model()
        return user.objects.create_superuser(
            'test',
            email='testuser@test.com',
            password='test'
        )

    # Проверка доступности урла сервиса, без/с токеном авторизации.
    def test_view_url_exists_and_unauthorized_answer(self):
        response = self.client.get('/api/v1/discount')
        self.assertEqual(response.status_code, 401)

    def test_view_url_exists_and_authorized_answer(self):
        response = self.response_for_positive_amount
        self.assertEqual(response.status_code, 200)

    # Проверка финальных сумм, где сумма корзины больше/меньше суммы промокода.
    def test_calculate_discount_amount_for_response_positive(self):
        response = self.response_for_positive_amount
        self.assertEqual(response.data['amount_cart'], 1.00)

    def test_calculate_discount_amount_for_response_negative(self):
        response = self.response_for_negative_amount
        self.assertEqual(response.data['amount_cart'], 0.00)

