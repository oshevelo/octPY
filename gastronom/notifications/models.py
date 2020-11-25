from django.db import models
from django.contrib.auth.models import User

# import logging

from gastronom.settings import INSTALLED_APPS
from notifications.sender import send_methods


# logger = logging.getLogger('__name__')


class Notification(models.Model):
    SOURCE = [(x, x) for x in INSTALLED_APPS]
    source = models.CharField(max_length=200, choices=SOURCE)
    recipient = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='notifications')
    send_methods = (
        ('email', 'E-mail'),
        ('telegram', 'Telegram'),
        ('viber', 'Viber'),
        ('sms', 'sms'),
        ('site', 'Site'),
    )
    send_method = models.CharField(choices=send_methods, default='email', max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.TextField(max_length=50, default='GASTRONOM info')
    message = models.TextField(max_length=200)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.source} {self.recipient} {self.subject} {self.message} {self.timestamp} {self.send_method}"

    @classmethod
    def create_notifications(cls, source, recipient, message, send_method='email', subject='GASTRONOM info'):
        """
        Create and save notification objects to database
        :param source: str, name of app making notification
        :param recipient: class User object or list of class User objects
        :param subject: str, subject of notification
        :param message: str, body of notification message
        :param send_method: str, name of send method
        """
        if send_method in send_methods:
            send_func = send_methods[send_method]
            if isinstance(recipient, list):
                for user in recipient:
                    Notification.objects.create(
                        source=source,
                        recipient=user,
                        subject=subject,
                        message=message,
                        send_method=send_method,
                        )
                    send_func(recipient_email=user.email, message=message)
            else:
                Notification.objects.create(
                    source=source,
                    recipient=recipient,
                    message=message,
                    send_method=send_method,
                )
                send_func(recipient_email=str(recipient.email), message=message)
        else:
            pass
            # logger.error('Invalid method passed to the create_notifications')


# Example: Notification.create_notifications('notifications', recipient=[User.objects.get(id=1),
# User.objects.get(id=4)], message='This is my first e-mail notification from Django.gastronom', send_method='email')


class TelegramUser(models.Model):
    telegram_id = models.PositiveIntegerField(verbose_name='Telegram User ID', unique=True)
    # telegram_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    telegram_user_name = models.TextField(verbose_name='Telegram User Name', null=True, blank=True)
    telegram_user_phone = models.TextField(verbose_name='Telegram user phone number', null=True, blank=True)

    def __str__(self):
        return f'{self.telegram_id} {self.telegram_user_name} {self.telegram_user_phone}'


class TelegramIncomeMessage(models.Model):
    telegramuser = models.ForeignKey(TelegramUser, on_delete=models.PROTECT)
    text = models.TextField(verbose_name='Text')
    created_at = models.DateTimeField(verbose_name='Send time', auto_now_add=True)

    def __str__(self):
        return f'Message {self.pk} from {self.telegramuser}: {self.text} {self.created_at}'

    class Meta:
        verbose_name = 'Telegram income message'
