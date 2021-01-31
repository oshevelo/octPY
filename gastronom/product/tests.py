from django.test import TestCase, Client
from django.contrib.auth.models import User

from rest_framework.test import APIClient

from product.models import Product, ProductMedia, Characteristic
from catalog.models import Catalog


class ProductTestAPI(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_user(username="super", email="super@test.ua", is_superuser=True, password="super123")
        self.simpleuser = User.objects.create_user(username="simple", email="simple@test.ua", is_active=True, password="simple123")
        self.category = Catalog.objects.create(name='TestCategory')


        self.product = Product.objects.create(
            name="TestProduct",
            descriptions="some descriptions",
            raiting=5,
            productcount=10,
            price="777.99",
            sku="S0me124",
            available=True)

        self.characteristics = Characteristic.objects.create(
            product=self.product,
            characteristic='Test characteristic',
            descriptions='Test description characteristic')
        
        self.superclient = APIClient(username="super")
        self.superclient.login(username="super", password="super123")

        self.simpleclient = APIClient()
        self.simpleclient.login(username="simple", password="simple123")

        self.otherclient = Client()
        self.otherclient.login()

        
    def test_get_product_list_superuser(self):
        response = self.superclient.get(path='/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'count' : 1,
            'next' : None,
            'previous' : None,
            'results' : [
                {
                'id' : self.product.id,
                'name' : self.product.name,
                'categories' : [],
                'mediafiles' : [],
                'sku' : self.product.sku,
                'descriptions' : self.product.descriptions,
                'raiting' : self.product.raiting,
                'productcount' : self.product.productcount,
                'price' : self.product.price,
                'available' : self.product.available,
                'characteristics' : [{
                    'id' : self.characteristics.id,
                    'characteristic' : self.characteristics.characteristic,
                    'descriptions' : self.characteristics.descriptions
                }]
            }]
        })

    def test_get_product_list_simpleuser(self):
        response = self.simpleclient.get(path='/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'count' : 1,
            'next' : None,
            'previous' : None,
            'results' : [
                {
                'id' : self.product.id,
                'name' : self.product.name,
                'categories' : [],
                'mediafiles' : [],
                'sku' : self.product.sku,
                'descriptions' : self.product.descriptions,
                'raiting' : self.product.raiting,
                'productcount' : self.product.productcount,
                'price' : self.product.price,
                'available' : self.product.available,
                'characteristics' : [{
                    'id' : self.characteristics.id,
                    'characteristic' : self.characteristics.characteristic,
                    'descriptions' : self.characteristics.descriptions
                }]
            }]
        })

    
    def test_get_product_list_othereuser(self):
        response = self.otherclient.get(path='/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'count' : 1,
            'next' : None,
            'previous' : None,
            'results' : [
                {
                'id' : self.product.id,
                'name' : self.product.name,
                'categories' : [],
                'mediafiles' : [],
                'sku' : self.product.sku,
                'descriptions' : self.product.descriptions,
                'raiting' : self.product.raiting,
                'productcount' : self.product.productcount,
                'price' : self.product.price,
                'available' : self.product.available,
                'characteristics' : [{
                    'id' : self.characteristics.id,
                    'characteristic' : self.characteristics.characteristic,
                    'descriptions' : self.characteristics.descriptions
                }]
            }]
        })


    
    def test_post_product_superuser(self):
        response = self.superclient.post('/products/', 
            {
                'name' : 'TestSuperProduct',
                'sku' : 'super123',
                'categories' : self.category.id,
                'descriptions' : 'some super',
                'raiting' : 4.1,
                'productcount' : 20,
                'price' : '14.88',
                'available' : True,
            })
        self.assertEqual(response.status_code, 201)


    def test_post_product_simpleuser(self):
        response = self.simpleclient.post('/products/', 
            {
                'name' : 'TestSuperProduct',
                'sku' : 'super123',
                'categories' : self.category.id,
                'descriptions' : 'some super',
                'raiting' : 4.1,
                'productcount' : 20,
                'price' : '14.88',
                'available' : True,
            })
        
        self.assertEqual(response.status_code, 403)

    
    def test_post_product_otherclient(self):
        response = self.otherclient.post('/products/', 
            {
                'name' : 'TestSuperProduct',
                'sku' : 'super123',
                'categories' : self.category.id,
                'descriptions' : 'some super',
                'raiting' : 4.1,
                'productcount' : 20,
                'price' : '14.88',
                'available' : True,
            })
        self.assertEqual(response.status_code, 401)

    
    def test_post_characteristic_superuser(self):
        response = self.superclient.post(f'/products/{self.product.id}/characteristics/',
            {
                'characteristic' : 'New characteristic',
                'descriptions' : 'New descriptions'

            })
        self.assertEqual(response.status_code, 201)

    
    def test_post_characteristic_simpleuser(self):
        response = self.simpleclient.post(f'/products/{self.product.id}/characteristics/',
            {
                'characteristic' : 'New characteristic',
                'descriptions' : 'New descriptions'

            })
        self.assertEqual(response.status_code, 403)

    
    def test_post_characteristic_otheruser(self):
        response = self.otherclient.post(f'/products/{self.product.id}/characteristics/',
            {
                'characteristic' : 'New characteristic',
                'descriptions' : 'New descriptions'

            })
        self.assertEqual(response.status_code, 401)