from collections import OrderedDict

from django.core import mail
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from rest_framework.test import APIClient

from gastronom.settings import CHAT_ID
from notifications.models import Notification, TelegramIncomeMessage, TelegramReplyMessage, TelegramUser
from notifications.views import create_notifications
from user_profile.models import UserProfile


class NotificationTest(TestCase):

    def setUp(self):
        # create 3 levels of access to data: 1st(super) - full access, 2nd(staff) - read only, 3rd(active, or any other) - no access
        self.superuser = User.objects.create_user(username='OksanaSUPER', email='o.ieroshenko@gmail.com', is_superuser=True, password='12345')
        self.staffuser = User.objects.create_user(username='OksanaSTAFF', email='o.ieroshenko@gmail.com', is_staff=True, password='12345')
        self.otheruser = User.objects.create_user(username='OksanaOTHER', email='o.ieroshenko@gmail.com', is_active=True, password='12345')

        self.notification_1 = Notification.objects.create(source='notifications', recipient=User.objects.get(username='OksanaSUPER'),
                                                          message='message message message')
        self.notification_2 = Notification.objects.create(source='notifications', recipient=User.objects.get(username='OksanaSUPER'),
                                                          message='message message message', subject='other', send_method='telegram')
        # for put and patch any object in nested data must be API client
        self.superclient = APIClient(username='OksanaSUPER')
        self.superclient.login(username='OksanaSUPER', password='12345')

        self.staffclient = Client(username='OksanaSTAFF')
        self.staffclient.login(username='OksanaSTAFF', password='12345')

        self.otherclient = Client()
        self.otherclient.login()

    def test_return_values(self):
        assert isinstance(self.notification_1, Notification)
        assert isinstance(self.notification_2, Notification)

        assert str(self.notification_1) == f'False None notifications OksanaSUPER GASTRONOM info message message message ' \
                                           f'{self.notification_1.timestamp} email'
        assert str(self.notification_2) == f'False None notifications OksanaSUPER other message message message {self.notification_2.timestamp}' \
                                           f' telegram'

    def test_NotificationListCreate(self):
        # get method:
        res = self.superclient.get(path='/notifications/last/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 2),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', res.data['results'][0]['id']),
                                                                         ('is_sent', False),
                                                                         ('sent_time', None),
                                                                         ('source', 'notifications'),
                                                                         ('recipient', res.data['results'][0]['recipient']),
                                                                         ('message', 'message message message'),
                                                                         ('timestamp', res.data['results'][0]['timestamp']),
                                                                         ('send_method', 'telegram')]),
                                                             OrderedDict([('id', res.data['results'][1]['id']),
                                                                         ('is_sent', False),
                                                                         ('sent_time', None),
                                                                         ('source', 'notifications'),
                                                                         ('recipient', res.data['results'][1]['recipient']),
                                                                         ('message', 'message message message'),
                                                                         ('timestamp', res.data['results'][1]['timestamp']),
                                                                         ('send_method', 'email')])])]))

        res = self.staffclient.get(path='/notifications/last/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 2),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', res.data['results'][0]['id']),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][0]['recipient']),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][0]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', res.data['results'][1]['id']),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][1]['recipient']),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][1]['timestamp']),
                                                                          ('send_method', 'email')])])]))

        res = self.otherclient.get(path='/notifications/last/')
        self.assertEqual(res.status_code, 404)

        # post method:
        res = self.superclient.post(path=f'/notifications/last/',
                                    data={'source': 'comments', 'message': 'comments post', 'recipient': f'{self.superuser.id}'})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['is_sent'], False)
        self.assertEqual(res.data['sent_time'], None)
        self.assertEqual(res.data['source'], 'comments')
        self.assertEqual(res.data['recipient'], self.superuser.id)
        self.assertEqual(res.data['message'], 'comments post')
        self.assertEqual(res.data['send_method'], f'email')

        res = self.staffclient.post(path=f'/notifications/last/',
                                    data={'source': 'comments', 'message': 'comments post', 'recipient': f'{self.superuser.id}'})
        self.assertEqual(res.status_code, 404)

        res = self.otherclient.post(path=f'/notifications/last/',
                                    data={'source': 'comments', 'message': 'comments post', 'recipient': f'{self.superuser.id}'})
        self.assertEqual(res.status_code, 404)

    def test_NotificationsByRecipient(self):
        # get method:
        res = self.superclient.get(path=f'/notifications/recipient/{self.superuser.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 2),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', res.data['results'][0]['id']),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][0]['recipient']),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][0]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', res.data['results'][1]['id']),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][1]['recipient']),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][1]['timestamp']),
                                                                          ('send_method', 'email')])])]))

        res = self.staffclient.get(path=f'/notifications/recipient/{self.superuser.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 2),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', res.data['results'][0]['id']),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][0]['recipient']),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][0]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', res.data['results'][1]['id']),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][1]['recipient']),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][1]['timestamp']),
                                                                          ('send_method', 'email')])])]))

        res = self.otherclient.get(path=f'/notifications/recipient/{self.superuser.id}/')
        self.assertEqual(res.status_code, 404)

        # post method:
        res = self.superclient.post(path=f'/notifications/recipient/{self.superuser.id}/',
                                    data={'source': 'notifications', 'message': 'post', 'recipient': f'{self.superuser.id}'})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['is_sent'], False)
        self.assertEqual(res.data['sent_time'], None)
        self.assertEqual(res.data['source'], 'notifications')
        self.assertEqual(res.data['recipient'], self.superuser.id)
        self.assertEqual(res.data['message'], 'post')
        self.assertEqual(res.data['send_method'], 'email')

        res = self.staffclient.post(path=f'/notifications/recipient/{self.superuser.id}/',
                                    data={'source': 'notifications', 'message': 'post', 'recipient': f'{self.superuser.id}'})
        self.assertEqual(res.status_code, 404)

        res = self.otherclient.post(path=f'/notifications/recipient/{self.superuser.id}/',
                                    data={'source': 'notifications', 'message': 'post', 'recipient': f'{self.superuser.id}'})
        self.assertEqual(res.status_code, 404)

    def test_NotificationsUnsent(self):
        # get method:
        res = self.superclient.get(path='/notifications/unsent/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 2),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', self.notification_2.id),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', self.superuser.id),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][0]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', self.notification_1.id),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', self.superuser.id),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][1]['timestamp']),
                                                                          ('send_method', 'email')])])]))

        res = self.staffclient.get(path='/notifications/unsent/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 2),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', self.notification_2.id),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', self.superuser.id),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][0]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', self.notification_1.id),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', self.superuser.id),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][1]['timestamp']),
                                                                          ('send_method', 'email')])])]))

        res = self.otherclient.get(path='/notifications/unsent/')
        self.assertEqual(res.status_code, 404)

        # post method:
        res = self.superclient.post(path=f'/notifications/unsent/',
                                    data={'source': 'comments', 'message': 'unsent post', 'recipient': f'{self.superuser.id}', 'is_sent': True,
                                          'send_method': 'telegram'})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['is_sent'], True)
        self.assertEqual(res.data['sent_time'], None)
        self.assertEqual(res.data['source'], 'comments')
        self.assertEqual(res.data['recipient'], self.superuser.id)
        self.assertEqual(res.data['message'], 'unsent post')
        self.assertEqual(res.data['send_method'], 'telegram')

        res = self.staffclient.post(path=f'/notifications/unsent/',
                                    data={'source': 'comments', 'message': 'unsent post', 'recipient': f'{self.superuser.id}', 'is_sent': True,
                                          'send_method': 'telegram'})
        self.assertEqual(res.status_code, 404)

        res = self.otherclient.post(path=f'/notifications/unsent/',
                                    data={'source': 'comments', 'message': 'unsent post', 'recipient': f'{self.superuser.id}', 'is_sent': True,
                                          'send_method': 'telegram'})
        self.assertEqual(res.status_code, 404)

    def test_NotificationsByUserNested(self):
        # get method:
        res = self.superclient.get(path=f'/notifications/recipient/{self.superuser.id}/nested/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, {'id': self.superuser.id,
                                    'username': 'OksanaSUPER',
                                    'notifications': [OrderedDict([('id', self.notification_2.id),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', self.notification_2.recipient_id),
                                                                   ('message', 'message message message'),
                                                                   ('timestamp', res.data['notifications'][0]['timestamp']),
                                                                   ('send_method', 'telegram')]),
                                                      OrderedDict([('id', self.notification_1.id),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', self.notification_1.recipient_id),
                                                                   ('message', 'message message message'),
                                                                   ('timestamp', res.data['notifications'][1]['timestamp']),
                                                                   ('send_method', 'email')])]})

        res = self.staffclient.get(path=f'/notifications/recipient/{self.superuser.id}/nested/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, {'id': self.superuser.id,
                                    'username': 'OksanaSUPER',
                                    'notifications': [OrderedDict([('id', self.notification_2.id),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', self.notification_2.recipient_id),
                                                                   ('message', 'message message message'),
                                                                   ('timestamp', res.data['notifications'][0]['timestamp']),
                                                                   ('send_method', 'telegram')]),
                                                      OrderedDict([('id', self.notification_1.id),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', self.notification_1.recipient_id),
                                                                   ('message', 'message message message'),
                                                                   ('timestamp', res.data['notifications'][1]['timestamp']),
                                                                   ('send_method', 'email')])]})

        res = self.otherclient.get(path=f'/notifications/recipient/{self.superuser.id}/nested/')
        self.assertEqual(res.status_code, 404)

        # put method:
        put_data = {'id': 2, 'username': 'OksanaSUPER', 'notifications': [OrderedDict([('id', self.notification_2.id),
                                                                                       ('is_sent', False),
                                                                                       ('sent_time', None),
                                                                                       ('source', 'notifications'),
                                                                                       ('recipient', self.notification_2.recipient_id),
                                                                                       ('message', '333333333333333333333333333333'),
                                                                                       ('timestamp', None),
                                                                                       ('send_method', 'telegram')]),
                                                                          OrderedDict([('id', self.notification_1.id),
                                                                                       ('is_sent', False),
                                                                                       ('sent_time', None),
                                                                                       ('source', 'notifications'),
                                                                                       ('recipient', self.notification_1.recipient_id),
                                                                                       ('message', 'message message message'),
                                                                                       ('timestamp', self.notification_1.timestamp),
                                                                                       ('send_method', 'email')])]}

        res = self.superclient.put(path=f'/notifications/recipient/{self.superuser.id}/nested/', data=put_data, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, {'id': self.superuser.id,
                                    'username': 'OksanaSUPER',
                                    'notifications': [OrderedDict([('id', res.data['notifications'][0]['id']),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', res.data['notifications'][0]['recipient']),
                                                                   ('message', '333333333333333333333333333333'),
                                                                   ('timestamp', res.data['notifications'][0]['timestamp']),
                                                                   ('send_method', 'telegram')]),
                                                      OrderedDict([('id', res.data['notifications'][1]['id']),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', res.data['notifications'][1]['recipient']),
                                                                   ('message', 'message message message'),
                                                                   ('timestamp', res.data['notifications'][1]['timestamp']),
                                                                   ('send_method', 'email')])]})

        res = self.staffclient.put(path=f'/notifications/recipient/{self.superuser.id}/nested/', data=put_data, format='json')
        self.assertEqual(res.status_code, 404)

        res = self.otherclient.put(path=f'/notifications/recipient/{self.superuser.id}/nested/', data=put_data, format='json')
        self.assertEqual(res.status_code, 404)

        # patch method:
        patch_data = {'notifications': [{'notification_id': self.notification_2.id, 'source': 'notifications', 'message': '7777777777777777777777'}]}
        res = self.superclient.patch(path=f'/notifications/recipient/{self.superuser.id}/nested/', data=patch_data, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, {'id': res.data['id'],
                                    'username': 'OksanaSUPER',
                                    'notifications': [OrderedDict([('id', res.data['notifications'][0]['id']),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', res.data['notifications'][0]['recipient']),
                                                                   ('message', '7777777777777777777777'),
                                                                   ('timestamp', res.data['notifications'][0]['timestamp']),
                                                                   ('send_method', 'email')])]})

        res = self.staffclient.patch(path=f'/notifications/recipient/{self.superuser.id}/nested/', data=patch_data, format='json')
        self.assertEqual(res.status_code, 404)

        res = self.otherclient.patch(path=f'/notifications/recipient/{self.superuser.id}/nested/', data=patch_data, format='json')
        self.assertEqual(res.status_code, 404)

        # delete method:
        res = self.superclient.delete(path=f'/notifications/recipient/{self.superuser.id}/nested/')
        self.assertEqual(res.status_code, 204)
        res = self.superclient.get(path='/notifications/last/')
        self.assertEqual(res.status_code, 404)

        res = self.superclient.delete(path=f'/notifications/recipient/{self.superuser.id}/nested/')
        self.assertEqual(res.status_code, 404)

        res = self.superclient.delete(path=f'/notifications/recipient/{self.superuser.id}/nested/')
        self.assertEqual(res.status_code, 404)

    def test_create_notifications(self):
        # create_notifications with only required fields
        create_notifications(source='notifications', recipients=[user for user in User.objects.all()], message='to all users')
        res = self.superclient.get(path='/notifications/last/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 5),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', res.data['results'][0]['id']),
                                                                          ('is_sent', True),
                                                                          ('sent_time', res.data['results'][0]['sent_time']),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][0]['recipient']),
                                                                          ('message', 'to all users'),
                                                                          ('timestamp', res.data['results'][0]['timestamp']),
                                                                          ('send_method', 'email')]),
                                                             OrderedDict([('id', res.data['results'][1]['id']),
                                                                          ('is_sent', True),
                                                                          ('sent_time', res.data['results'][1]['sent_time']),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][1]['recipient']),
                                                                          ('message', 'to all users'),
                                                                          ('timestamp', res.data['results'][1]['timestamp']),
                                                                          ('send_method', 'email')]),
                                                             OrderedDict([('id', res.data['results'][2]['id']),
                                                                          ('is_sent', True),
                                                                          ('sent_time', res.data['results'][2]['sent_time']),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][2]['recipient']),
                                                                          ('message', 'to all users'),
                                                                          ('timestamp', res.data['results'][2]['timestamp']),
                                                                          ('send_method', 'email')]),
                                                             OrderedDict([('id', res.data['results'][3]['id']),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][3]['recipient']),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][3]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', res.data['results'][4]['id']),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][4]['recipient']),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][4]['timestamp']),
                                                                          ('send_method', 'email')])])])
)
        # create_notifications with giving all fields
        create_notifications(source='comments', recipients=[self.superuser], message='to user', subject='some subject', send_method='telegram')
        res = self.superclient.get(path='/notifications/last/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 6),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', res.data['results'][0]['id']),
                                                                          ('is_sent', True),
                                                                          ('sent_time', res.data['results'][0]['sent_time']),
                                                                          ('source', 'comments'),
                                                                          ('recipient', res.data['results'][0]['recipient']),
                                                                          ('message', 'to user'),
                                                                          ('timestamp', res.data['results'][0]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', res.data['results'][1]['id']),
                                                                          ('is_sent', True),
                                                                          ('sent_time', res.data['results'][1]['sent_time']),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][1]['recipient']),
                                                                          ('message', 'to all users'),
                                                                          ('timestamp', res.data['results'][1]['timestamp']),
                                                                          ('send_method', 'email')]),
                                                             OrderedDict([('id', res.data['results'][2]['id']),
                                                                          ('is_sent', True),
                                                                          ('sent_time', res.data['results'][2]['sent_time']),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][2]['recipient']),
                                                                          ('message', 'to all users'),
                                                                          ('timestamp', res.data['results'][2]['timestamp']),
                                                                          ('send_method', 'email')]),
                                                             OrderedDict([('id', res.data['results'][3]['id']),
                                                                          ('is_sent', True),
                                                                          ('sent_time', res.data['results'][3]['sent_time']),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][3]['recipient']),
                                                                          ('message', 'to all users'),
                                                                          ('timestamp', res.data['results'][3]['timestamp']),
                                                                          ('send_method', 'email')]),
                                                             OrderedDict([('id', res.data['results'][4]['id']),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][4]['recipient']),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][4]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', res.data['results'][5]['id']),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', res.data['results'][5]['recipient']),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][5]['timestamp']),
                                                                          ('send_method', 'email')])])]))

        self.assertEqual(len(mail.outbox), 4)

        # check sending to telegram wuth create_notification function
        self.user_profile = UserProfile.objects.create(user=self.superuser, telegram_id=CHAT_ID)
        create_notifications(source='comments', recipients=[self.superuser], message='to user', subject='some subject', send_method='telegram')

    def test_NotificationAll(self):

        res = self.superclient.get(path='/notifications/all/')
        self.assertEqual(res.status_code, 200)

        res = self.staffclient.get(path='/notifications/all/')
        self.assertEqual(res.status_code, 200)

        res = self.client.get(path='/notifications/all/')
        self.assertEqual(res.status_code, 404)
