import logging

from django.db import models
from django.contrib.auth.models import User

from telegram.utils.request import Request
from telegram import Bot
from telegram.error import InvalidToken
from gastronom.settings import INSTALLED_APPS, TOKEN, PROXY_URL, CHAT_ID
from notifications.sender import send_methods


try:
    request = Request(connect_timeout=0.5, read_timeout=1.0, con_pool_size=8)
    bot = Bot(request=request, token=TOKEN, base_url=PROXY_URL)
except InvalidToken: 
    request = None
    bot = None  

logger = logging.getLogger(__name__)


class Notification(models.Model):
    SOURCE = [(x, x) for x in INSTALLED_APPS]
    source = models.CharField(max_length=200, choices=SOURCE)
    recipient = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='notifications')
    send_methods = (
        ('email', 'email'),
        ('telegram', 'telegram'),
        ('viber', 'viber'),
        ('sms', 'sms'),
        ('site', 'site'),
    )
    send_method = models.CharField(choices=send_methods, default='email', max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.TextField(max_length=50, default='GASTRONOM info')
    message = models.TextField(max_length=500)
    sent = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.sent} {self.source} {self.recipient} {self.subject} {self.message} {self.timestamp} {self.send_method}"

    @classmethod
    def create_notifications(cls, source, recipient, message, send_method='email', subject='GASTRONOM info'):
        """
        Create and save notification objects to database
        :param source: str, name of app making notification
        :param recipient: class User object or list of class User objects
        :param subject: str, subject of notification
        :param message: str, body of notification message
        :param send_method: str, name of send method

        Examples:
        from django.contrib.auth.models import User
        from notifications.models import Notification
        from user_profile.models import UserProfile

        email to list of Users:
        Notification.create_notifications('notifications', recipient=[User.objects.get(id=1), User.objects.get(id=4)], message='This is my 100500th e-mail notification from Django.gastronom', send_method='email', subject='My 100500 message')

        email to User:
        Notification.create_notifications('notifications', recipient=User.objects.get(id=1), message='This is my 100500th e-mail notification from Django.gastronom', send_method='email', subject='My 100500 message')

        telegram to list of Users:
        Notification.create_notifications('notifications', recipient=[User.objects.get(id=1), User.objects.get(id=4)], message='This is my 100500th e-mail notification from Django.gastronom', send_method='email', subject='My 100500 message')

        telegram to User:
        Notification.create_notifications('notifications', recipient=User.objects.get(id=1), message='Це моя перша телеграма from Django.gastronom', send_method='telegram')

        telegram to all Users:
        Notification.create_notifications('notifications', recipient=[user for user in User.objects.all()], message='Це моя перша телеграма from Django.gastronom', send_method='telegram')
        """
        if send_method in send_methods:
            send_func = send_methods[send_method]
            if isinstance(recipient, list):
                for user in recipient:
                    n = Notification(source=source, recipient=user, subject=subject, message=message, send_method=send_method)
                    try:
                        send_func(recipient=user, message=message, subject=subject)
                        n.sent = True
                        n.save()
                    except Exception as e:
                        logger.info(e)
                        bot.send_message(chat_id=CHAT_ID, text=str(e))
            else:
                n = Notification(source=source, recipient=recipient, subject=subject, message=message, send_method=send_method)
                try:
                    send_func(recipient, message, subject=subject)
                    n.sent = True
                    n.save()
                except Exception as e:
                    logger.info(e)
                    bot.send_message(chat_id=CHAT_ID, text=str(e))
        else:
            pass
            logger.error('Invalid send method passed to the create_notifications')


class TelegramUser(models.Model):
    chat_id = models.PositiveIntegerField(verbose_name='User ID', unique=True)
    username = models.TextField(verbose_name='User Name', null=True, blank=True, max_length=50)
    user_phone = models.TextField(verbose_name='User phone number', null=True, blank=True, max_length=50, unique=True)
    user_first_name = models.CharField(verbose_name='First name', null=True, blank=True, max_length=30)
    user_last_name = models.CharField(verbose_name='Last name', null=True, blank=True, max_length=30)

    def __str__(self):
        return f'{self.username} {self.user_phone} {self.user_first_name} {self.user_last_name} {self.chat_id}'

    class Meta:
        verbose_name = 'Telegram user'


class TelegramIncomeMessage(models.Model):
    telegramuser = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='User')
    text = models.TextField(verbose_name='Income message', max_length=200)
    date = models.DateTimeField(verbose_name='Date', auto_now_add=True)
    message_id = models.CharField(max_length=20, verbose_name='Message id')
    chat_id = models.CharField(max_length=20, null=True, blank=True, verbose_name='Chat_id')

    def __str__(self):
        return f'Message text: {self.text} from: {self.telegramuser}, datetime: ' \
               f''+'{:%d.%m.%y %H:%M}'.format(self.date)+f'id: {self.pk}'

    class Meta:
        verbose_name = 'Income message'


class TelegramReplyMessage(models.Model):
    reply_to_message = models.ForeignKey('TelegramIncomeMessage', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Income message')
    reply_message = models.TextField(max_length=200, verbose_name='Reply message')

    def __str__(self):
        return f'ReplyID: {self.pk}, to: {self.reply_to_message}, text: {self.reply_message}'

    class Meta:
        verbose_name = 'Reply message'
