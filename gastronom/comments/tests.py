from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from .models import Review
from gastronom.local_settings import TEST_PASSWORD

from rest_framework.test import APIClient

from PIL import Image
import tempfile

# Create your tests here.


class ReviewTestApi(TestCase):

    def setUp(self):

        self.superuser = User.objects.create_user(username='repka', email='', is_superuser=True, password=TEST_PASSWORD)
        self.buyer = User.objects.create_user(username='repkabuyer', email='', is_active=True, password=TEST_PASSWORD)

        self.superclient = APIClient(username='repka')
        self.superclient.login(username='repka', password=TEST_PASSWORD)
        self.buyerclient = Client()

        self.review_super = Review.objects.create(user=self.superuser, text='some text')
        self.review_buyer = Review.objects.create(user=self.buyer, text='some text')

    def generate_image(self):
        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(tmp_file)
        tmp_file.seek(0)
        return tmp_file

    def test_get_review_list_superuser_with_permission(self):
        response = self.superclient.get('/comments/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'count': 2, 'next': None, 'previous': None,
                                            'results': [
                                                {'user': {'username': self.superuser.username},
                                                'product': None, 'text': 'some text',
                                                'created': response.data['results'][0]['created'],
                                                'child': [], 'reply_to': None},
                                                {'user': {'username': self.buyer.username},
                                                'product': None, 'text': 'some text',
                                                'created': response.data['results'][1]['created'],
                                                'child': [], 'reply_to': None}]})

    def test_get_review_list_buyer_with_permission(self):
        response = self.buyerclient.get('/comments/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'count': 2, 'next': None, 'previous': None,
                                            'results': [
                                                {'user': {'username': self.buyer.username},
                                                'product': None, 'text': 'some text',
                                                'created': response.data['results'][0]['created'],
                                                'child': [], 'reply_to': None},
                                                {'user': {'username': self.superuser.username},
                                                'product': None, 'text': 'some text',
                                                'created': response.data['results'][1]['created'],
                                                'child': [], 'reply_to': None}]})

    def test_get_detail_review_buyer_with_permission(self):
        self.buyerclient.login()
        response = self.buyerclient.get(f'/comments/reviews/{self.review_buyer.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'user': {'username': self.buyer.username},
                                            'product': None, 'text': 'some text',
                                            'created': response.data['created'],
                                            'child': [], 'reply_to': None})

    def test_get_detail_review_buyer_without_permission(self):
        response = self.buyerclient.get(f'/comments/reviews/{self.review_buyer.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'user': {'username': self.buyer.username},
                                            'product': None, 'text': 'some text',
                                            'created': response.data['created'],
                                            'child': [], 'reply_to': None})

    def test_post_review_list_superuser_with_permission(self):
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

    def test_post_review_list_buyer_without_permission(self):
        response = self.buyerclient.post('/comments/reviews/', {'product': '',
                                                            'text': 'dadadad',
                                                            'child': []})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_post_image_buyer_with_permission(self):
        self.buyerclient.login(username='repkabuyer', password=TEST_PASSWORD)

        response = self.buyerclient.post('/comments/reviews-image/', {'raw_photo': self.generate_image(), 'review': self.review_buyer.id}, format='multipart')

        self.assertEqual(response.status_code, 201)
