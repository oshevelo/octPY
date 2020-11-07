from django.db import models
from django.contrib.auth import get_user_model


class Notification(models.Model):

    SENDER = (
        'ACTIVITIES',
        'ANALYTICS',
        'CART',
        'CATALOG',
        'COMMENTS',
        'INFO',
        'LOYALTY',
        'NOTIFICATIONS',
        'ORDER',
        'PAYMENT',
        'PRODUCT',
        'SHIPMENT',
        'USER_PROFILE',
    )
    sender = models.CharField(choices=SENDER)
    recipient = models.CharField
    method = models.CharField(default='e-mail')
    timestamp = models.DateTimeField(auto_now_add=True)
    verb = models.CharField()

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.sender} {self.recipient} {self.verb} {self.timestamp}"


def create_notifications(sender, recipient, verb, **kwargs):

    if recipient == "global":
        users = get_user_model().objects.all()
        for user in users:
            Notification.objects.create(
                sender=sender,
                recipient=user,
                verb=verb,
            )

    elif isinstance(recipient, list):
        for user in recipient:
            Notification.objects.create(
                sender=sender,
                recipient=get_user_model().objects.get(username=user),
                verb=verb,
            )

    elif isinstance(recipient, get_user_model()):
        Notification.objects.create(
            sender=sender,
            recipient=recipient,
            verb=verb,
        )
    else:
        pass
