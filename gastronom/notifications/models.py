from django.db import models
from django.contrib.auth.models import User
from gastronom.settings import INSTALLED_APPS
from notifications.sender import send_method_validator


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
        if send_method_validator(send_method):
            send_func = send_method_validator(send_method)
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


# Example: Notification.create_notifications('notifications', recipient=[User.objects.get(id=1),
# User.objects.get(id=4)], message='This is my first e-mail notification from Django.gastronom', send_method='email')


class TelegramUser(models.Model):
    telegram_id = models.PositiveIntegerField(verbose_name='Telegram User ID', unique=True)
    # telegram_user = models.ForeignKey(User, on_delete=models.CASCADE)
    telegram_user_name = models.TextField(verbose_name='Telegram User Name', default='')

    def __str__(self):
        return f'#{self.telegram_id} {self.telegram_user.username}'
