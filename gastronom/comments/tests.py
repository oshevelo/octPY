from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Review, ReviewImage

from rest_framework.test import APIClient


# Create your tests here.


class ReviewTestApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='repka', email='',
                                                password='life230493')
        self.client.login(username='repka', password='life230493')
        self.review_1 = Review.objects.create(user=self.user, text='some text')

    def test_get_review_list_with_permission(self):
        response = self.client.get('/comments/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'count': 1, 'next': None,
                                            'previous': None,
                                            'results': [{
                                                'user': {'username': 'repka'},
                                                'product': None,
                                                'text': 'some text',
                                                'created': response.data['results'][0]['created'],
                                                'child': [],
                                                'reply_to': None
                                                }]})

    def test_post_review_list_with_permission(self):
        response = self.client.post('/comments/reviews/', {'product': '',
                                                            'text': 'some text',
                                                            'child': []})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'child': [],
                                           'created': response.data['created'],
                                           'product': None,
                                           'reply_to': None,
                                           'text': 'some text',
                                           'user': {'username': 'repka'}})
