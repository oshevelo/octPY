from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User

from .models import Cart, CartItem
from product.models import Product


class CartTestCase(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name='some_product',
                                              price=228,
                                              count=100)

        self.super_user = User.objects.create_user(username='super_user', email='super_user@iii.iii', password='1337',
                                                   is_superuser=True)
        self.staff_user = User.objects.create_user(username='staff_user', email='staff_user@iii.iii', password='1337',
                                                   is_staff=True)
        self.customer = User.objects.create_user(username='customer', email='customer@iii.iii', password='1337',
                                                 is_active=True)

        self.super_user_cart = Cart.objects.create(user=self.super_user)
        self.staff_user_cart = Cart.objects.create(user=self.staff_user)
        self.customer_cart = Cart.objects.create(user=self.customer)

        self.super_cartitem = CartItem.objects.create(product=self.product,
                                                      cart=self.super_user_cart,)
        self.staff_cartitem = CartItem.objects.create(product=self.product,
                                                      cart=self.staff_user_cart,)
        self.customer_cartitem = CartItem.objects.create(product=self.product,
                                                         cart=self.customer_cart,)

        self.super_user_client = APIClient()
        self.staff_user_client = APIClient()
        self.customer_client = APIClient()

    def test_create_cart(self):
        self.super_user_client.login(username='super_user', password='1337')
        self.staff_user_client.login(username='staff_user', password='1337')
        self.customer_client.login(username='customer', password='1337')

        super_user_res = self.super_user_client.get('/cart/1/')
        staff_user_res = self.staff_user_client.get('/cart/2/')
        customer_res = self.customer_client.get('/cart/3/')

        self.assertEqual(super_user_res.json(), {
             'id': 1,
             'user': 1,
             'creation_date': self.super_user_cart.creation_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
             'total_price': 228.0,
             'cart_items': [{'amount_left': 100,
                             'cart': 1,
                             'id': 1,
                             'product': 1,
                             'quantity': 1,
                             'unit_price': 228.0}]})

        self.assertEqual(customer_res.json(), {'detail': 'You do not have permission to perform this action.'})

        self.assertEqual(super_user_res.status_code, 200)
        self.assertEqual(staff_user_res.status_code, 200)
        self.assertEqual(customer_res.status_code, 403)

    def test_create_cartitem(self):
        print(f'\nuserID: {self.super_user.id}, cartID: {self.super_user_cart.id}, cartitemID: {self.super_cartitem.id}'
              f'\nuserID: {self.staff_user.id}, cartID: {self.staff_user_cart.id}, cartitemID: {self.staff_cartitem.id}'
              f'\nuserID: {self.customer.id}, cartID: {self.customer_cart.id}, cartitemID: {self.customer_cartitem.id}')

        self.super_user_client.login(username='super_user', password='1337')
        self.staff_user_client.login(username='staff_user', password='1337')
        self.customer_client.login(username='customer', password='1337')

        super_user_res = self.super_user_client.get('/cart/1/cart_item/4/')
        staff_user_res = self.staff_user_client.get('/cart/2/cart_item/5/')
        customer_res = self.customer_client.get('/cart/3/cart_item/6/')

        self.assertEqual(super_user_res.json(), {'id': 4,
                                                 'cart': 4,
                                                 'product': 2,
                                                 'quantity': 1,
                                                 'unit_price': 228.0,
                                                 'amount_left': 100})
        self.assertEqual(staff_user_res.json(), {'id': 5,
                                                 'cart': 5,
                                                 'product': 2,
                                                 'quantity': 1,
                                                 'unit_price': 228.0,
                                                 'amount_left': 100})
        self.assertEqual(customer_res.json(), {'detail': 'You do not have permission to perform this action.'})
