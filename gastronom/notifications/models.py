from django.db import models
from django.contrib.auth.models import User
from gastronom.settings import INSTALLED_APPS
from notifications.sender import send_email


class Notification(models.Model):
    SOURCE = [(x, x) for x in INSTALLED_APPS]
    source = models.CharField(max_length=200, choices=SOURCE)
    recipient = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='notifications')
    send_methods = (
        ('email', 'E-mail'),
        ('messenger', 'Messenger'),
        ('site', 'Site'),
    )
    send_method = models.CharField(choices=send_methods, default='email', max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=200)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.source} {self.recipient} {self.message} {self.timestamp} {self.send_method}"

    @classmethod
    def create_notifications(cls, source, recipient, message, send_method):
        """
        Create and save notification objects to database
        :param source: str, name of app making notification
        :param recipient: class User object or list of class User objects
        :param message: str, body of notification message
        :param send_method: str, name of send method
        """
        if send_method == 'email':
            send_func = send_email

        if isinstance(recipient, list):
            for user in recipient:
                Notification.objects.create(
                    source=source,
                    recipient=user,
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


# Notification.create_notifications('notifications', recipient=[User.objects.get(id=1), User.objects.get(id=4)],
# message='Subject: Hi there \n\n This is my first e-mail notification from Django.gastronom', send_method='email')
