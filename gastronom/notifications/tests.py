from collections import OrderedDict

from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from notifications.models import Notification, TelegramIncomeMessage, TelegramReplyMessage, TelegramUser
from notifications.views import create_notifications


class NotificationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='OksanaYeroshenko', email='o.ieroshenko@gmail.com', is_superuser = True, password='12345')
        self.notification_1 = Notification.objects.create(source='notifications', recipient=User.objects.get(username='OksanaYeroshenko'),
                                                        message='message message message')
        self.notification_2 = Notification.objects.create(source='notifications', recipient=User.objects.get(username='OksanaYeroshenko'),
                                                          message='message message message', subject='other', send_method='telegram')
        self.client = Client(username='Oksanayeroshenko')
        self.client.login(username='OksanaYeroshenko', password='12345')

    def test_return_values(self):
        assert isinstance(self.notification_1, Notification)
        assert isinstance(self.notification_2, Notification)
        assert str(self.notification_1) == f'False None notifications OksanaYeroshenko GASTRONOM info message message message ' \
                                           f'{self.notification_1.timestamp} email'
        assert str(self.notification_2) == f'False None notifications OksanaYeroshenko other message message message {self.notification_2.timestamp}' \
                                           f' telegram'

    def test_NotificationListCreate(self):
        res = self.client.get(path='/notifications/last/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 2),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', 2),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', 1),
                                                                   ('message', 'message message message'),
                                                                   ('timestamp', res.data['results'][0]['timestamp']),
                                                                   ('send_method', 'telegram')]),
                                                      OrderedDict([('id', 1),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', 1),
                                                                   ('message', 'message message message'),
                                                                   ('timestamp', res.data['results'][1]['timestamp']),
                                                                   ('send_method', 'email')])])]))
        res = self.client.post(path=f'/notifications/last/',
                               data={'source': 'comments', 'message': 'comments post', 'recipient': f'{self.user.id}'})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['is_sent'], False)
        self.assertEqual(res.data['sent_time'], None)
        self.assertEqual(res.data['source'], 'comments')
        self.assertEqual(res.data['recipient'], self.user.id)
        self.assertEqual(res.data['message'], 'comments post')
        self.assertEqual(res.data['send_method'], f'email')

    def test_NotificationsByRecipient(self):
        res = self.client.get(path=f'/notifications/recipient/{self.user.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 2),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', 5),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', 2),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][0]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', 4),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', 2),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][1]['timestamp']),
                                                                          ('send_method', 'email')])])]))

        res = self.client.post(path=f'/notifications/recipient/{self.user.id}/',
                               data={'source': 'notifications', 'message': 'post', 'recipient': f'{self.user.id}'})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['is_sent'], False)
        self.assertEqual(res.data['sent_time'], None)
        self.assertEqual(res.data['source'], 'notifications')
        self.assertEqual(res.data['recipient'], self.user.id)
        self.assertEqual(res.data['message'], 'post')
        self.assertEqual(res.data['send_method'], 'email')

        # why do we need it for?

        # res = self.client.head(path=f'/notifications/recipient/{self.user.id}/')
        # print(res)
        # print(res.status_code)
        # print(res.data)
        # res = self.client.options(path=f'/notifications/recipient/{self.user.id}/')
        # print(res)
        # print(res.status_code)
        # print(res.data)

        # why i cannot delete?
        # res = self.client.delete(path=f'/notifications/recipient/{self.user.id}/')
        # print(res)
        # print(res.status_code)
        # print(res.data)

        # < Response
        # status_code = 405, "application/json" >
        # 405
        # {'detail': ErrorDetail(string='Method "DELETE" not allowed.', code='method_not_allowed')}

    def test_NotificationsUnsent(self):
        res = self.client.get(path='/notifications/unsent/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 2),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', self.notification_2.id),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', self.user.id),
                                                                   ('message', 'message message message'),
                                                                   ('timestamp', res.data['results'][0]['timestamp']),
                                                                   ('send_method', 'telegram')]),
                                                      OrderedDict([('id', self.notification_1.id),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', self.user.id),
                                                                   ('message', 'message message message'),
                                                                   ('timestamp', res.data['results'][1]['timestamp']),
                                                                   ('send_method', 'email')])])]))
        res = self.client.post(path=f'/notifications/unsent/',
                               data={'source': 'comments', 'message': 'unsent post', 'recipient': f'{self.user.id}', 'is_sent': True,
                                     'send_method': 'telegram'})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['is_sent'], True)
        self.assertEqual(res.data['sent_time'], None)
        self.assertEqual(res.data['source'], 'comments')
        self.assertEqual(res.data['recipient'], self.user.id)
        self.assertEqual(res.data['message'], 'unsent post')
        self.assertEqual(res.data['send_method'], 'telegram')

    def test_NotificationsByUserNested(self):
        res = self.client.get(path=f'/notifications/recipient/{self.user.id}/nested/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, {'id': self.user.id,
                                    'username': 'OksanaYeroshenko',
                                    'notifications': [OrderedDict([('id', self.notification_2.id),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', 3),
                                                                   ('message', 'message message message'),
                                                                   ('timestamp', res.data['notifications'][0]['timestamp']),
                                                                   ('send_method', 'telegram')]),
                                                      OrderedDict([('id', self.notification_1.id),
                                                                   ('is_sent', False),
                                                                   ('sent_time', None),
                                                                   ('source', 'notifications'),
                                                                   ('recipient', 3),
                                                                   ('message', 'message message message'),
                                                                   ('timestamp', res.data['notifications'][1]['timestamp']),
                                                                   ('send_method', 'email')])]})
        # res = self.client.post(path=f'/notifications/recipient/{self.user.id}/nested/',
        #                        data={'source': 'cart', 'message': 'nested post', 'recipient': f'{self.user.id}', 'send_method': 'site'})
        # print(res.data)
        # print(res)

        # ..django.request WARNING Method Not Allowed: / notifications / recipient / 3 / nested /
        # {'detail': ErrorDetail(string='Method "POST" not allowed.', code='method_not_allowed')}
        # < Response status_code = 405, "application/json" >

        # self.assertEqual(res.status_code, 201)
        # self.assertEqual(res.data['is_sent'], False)
        # self.assertEqual(res.data['sent_time'], None)
        # self.assertEqual(res.data['source'], 'cart')
        # self.assertEqual(res.data['recipient'], self.user.id)
        # self.assertEqual(res.data['message'], 'nested post')
        # self.assertEqual(res.data['send_method'], 'site')

    def test_create_notifications(self):
        USE_QUEUE = False
        create_notifications(source='notifications', recipients=[user for user in User.objects.all()], message='to all users')
        res = self.client.get(path='/notifications/last/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, OrderedDict([('count', 3),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', 14),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', 5),
                                                                          ('message', 'to all users'),
                                                                          ('timestamp', res.data['results'][0]['timestamp']),
                                                                          ('send_method', 'email')]),
                                                             OrderedDict([('id', 13),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', 5),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][1]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', 12), ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', 5),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][2]['timestamp']),
                                                                          ('send_method', 'email')])])]))
        create_notifications(source='comments', recipients=[self.user], message='to user', subject='some subject', send_method='telegram')
        res = self.client.get(path='/notifications/last/')
        self.assertEqual(res.status_code, 200)
        print(res.data)
        self.assertEqual(res.data, OrderedDict([('count', 4),
                                                ('next', None),
                                                ('previous', None),
                                                ('results', [OrderedDict([('id', 15),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'comments'),
                                                                          ('recipient', 5),
                                                                          ('message', 'to user'),
                                                                          ('timestamp', res.data['results'][0]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', 14),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', 5),
                                                                          ('message', 'to all users'),
                                                                          ('timestamp', res.data['results'][1]['timestamp']),
                                                                          ('send_method', 'email')]),
                                                             OrderedDict([('id', 13),
                                                                          ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', 5),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][2]['timestamp']),
                                                                          ('send_method', 'telegram')]),
                                                             OrderedDict([('id', 12), ('is_sent', False),
                                                                          ('sent_time', None),
                                                                          ('source', 'notifications'),
                                                                          ('recipient', 5),
                                                                          ('message', 'message message message'),
                                                                          ('timestamp', res.data['results'][3]['timestamp']),
                                                                          ('send_method', 'email')])])]))

# notifications.models.Notification.DoesNotExist: Notification matching query does not exist
