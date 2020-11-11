from django.db import models
from django.contrib.auth.models import User
from gastronom.settings import INSTALLED_APPS



class Notification(models.Model):

    SOURCE = [(x, x) for x in INSTALLED_APPS]
    source = models.CharField(max_length=200, choices=SOURCE)

    recipient = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    send_methods = (
        ('email', 'E-mail'),
        ('messenger', 'Messenger'),
        ('site', 'Site'),
    )
    send_method = models.CharField(choices=send_methods, default='email', max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    verb = models.CharField(max_length=200)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.source} {self.recipient} {self.verb} {self.timestamp} {self.send_method}"

    @classmethod
    def create_notifications(cls, source, recipient, verb, send_method):
        """
        Create and save notification objects to database
        :param source: str, name of app making notification
        :param recipient: class User object or list of class User objects
        :param verb: str, body of notification message
        :param send_method: str, name of send method
        """
        if isinstance(recipient, list):
            for user in recipient:
                Notification.objects.create(
                    source=source,
                    recipient=user,
                    verb=verb,
                    send_method=send_method,
                    ).save()

        else:
            Notification.objects.create(
                source=source,
                recipient=recipient,
                verb=verb,
                send_method=send_method,
            ).save()
