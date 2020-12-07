from django.test import TestCase
from django.test import Client

class NotificationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        print('setUp')

    def test_create_notification(self):
        """Animals that can speak are correctly identified"""
        res = self.client.get('/notifications/unsent/')
        print(res)
        print(res.data)
        print(res.status_code)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data, {'detail': "ErrorDetail(string='Not found.', code='not_found')"})

    def test_update_notification(self):
        """Animals that can speak are correctly identified"""

        self.assertEqual(1, 1)

    def test_uaapdate_notification(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual(1, 1)
