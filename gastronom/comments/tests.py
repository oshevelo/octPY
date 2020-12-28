from django.conf import settings
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Review, ReviewImage
from gastronom.local_settings import TEST_PASSWORD

from rest_framework.test import APIClient


# Create your tests here.


class ReviewTestApi(TestCase):

    def setUp(self):

        self.superuser = User.objects.create_user(username='repka', email='', is_superuser=True, password=TEST_PASSWORD)
        self.buyer = User.objects.create_user(username='repkabuyer', email='', is_active=True, password=TEST_PASSWORD)

        self.superclient = APIClient(username='repka')
        self.superclient.login(username='repka', password=TEST_PASSWORD)
        self.buyerclient = Client()
        self.buyerclient.login()

        self.review_super = Review.objects.create(user=self.superuser, text='some text')
        self.review_buyer = Review.objects.create(user=self.buyer, text='some text')

    def test_get_review_list_super_with_permission(self):
        response = self.superclient.get('/comments/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'count': 2, 'next': None, 'previous': None, 
                                            'results': [
                                                {'user': {'username': 'repka'}, 
                                                'product': None, 'text': 'some text', 
                                                'created': response.data['results'][0]['created'], 
                                                'child': [], 'reply_to': None},  
                                                {'user': {'username': 'repkabuyer'}, 
                                                'product': None, 'text': 'some text', 
                                                'created': response.data['results'][1]['created'], 
                                                'child': [], 'reply_to': None}]})
                                        
    def test_get_review_list_buyer_with_permission(self):
        response = self.buyerclient.get('/comments/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'count': 2, 'next': None, 'previous': None, 
                                            'results': [
                                                {'user': {'username': 'repka'}, 
                                                'product': None, 'text': 'some text', 
                                                'created': response.data['results'][0]['created'], 
                                                'child': [], 'reply_to': None},  
                                                {'user': {'username': 'repkabuyer'}, 
                                                'product': None, 'text': 'some text', 
                                                'created': response.data['results'][1]['created'], 
                                                'child': [], 'reply_to': None}]})

    def test_post_review_list_super_with_permission(self):
        response = self.superclient.post('/comments/reviews/', {'product': '',
                                                            'text': 'lalala',
                                                            'child': []})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'child': [],
                                           'created': response.data['created'],
                                           'product': None,
                                           'reply_to': None,
                                           'text': 'lalala',
                                           'user': {'username': 'repka'}})

    def test_post_review_list_buyer_with_permission(self):
        self.buyerclient = Client()
        self.buyerclient.login(username='repkabuyer', password=TEST_PASSWORD)
        response = self.buyerclient.post('/comments/reviews/', {'product': '',
                                                            'text': 'dadadad',
                                                            'child': []})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'child': [],
                                           'created': response.data['created'],
                                           'product': None,
                                           'reply_to': None,
                                           'text': 'dadadad',
                                           'user': {'username': 'repkabuyer'}})

