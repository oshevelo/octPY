import logging

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

logger = logging.getLogger(__name__)


class Notification(models.Model):
    SOURCE = (
        ('activity', 'activity'),
        ('analytics', 'analytics'),
        ('cart', 'cart'),
        ('catalog', 'catalog'),
        ('comments', 'comments'),
        ('discount', 'discount'),
        ('info', 'info'),
        ('loyalty', 'loyalty'),
        ('notifications', 'notifications'),
        ('order', 'order'),
        ('payment', 'payment'),
        ('product', 'product'),
        ('shipment', 'shipment'),
        ('user_profile', 'user_profile'),
        ('other_source', 'other_source')
    )
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
    is_sent = models.BooleanField(default=False, db_index=True)
    sent_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.is_sent} {self.sent_time} {self.source} {self.recipient} {self.subject} {self.message} {self.timestamp} {self.send_method}"


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
        return f'"{self.text}" FROM: {self.telegramuser.user_first_name} {self.telegramuser.user_last_name} '+'{:%d.%m.%y %H:%M:%S}'.format(
            self.date)

    class Meta:
        verbose_name = 'Income message'


class TelegramReplyMessage(models.Model):
    reply_to_message = models.ForeignKey('TelegramIncomeMessage', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Income message')
    reply_message = models.TextField(max_length=200, verbose_name='Reply message')
    is_sent = models.BooleanField(default=False, db_index=True)
    sent_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'ReplyID: {self.pk}, to: {self.reply_to_message}, text: {self.reply_message}'

    class Meta:
        verbose_name = 'Reply message'
