import logging

from django.core.mail import send_mail
from django.contrib.auth.models import User

from gastronom.settings import EMAIL_HOST_USER
from user_profile.models import UserProfile
from notifications.models import TelegramIncomeMessage
from notifications.bot import bot


logger = logging.getLogger(__name__)


def send_email(notification_obj):
    """
    Takes Notification object and sends it by its email.
    :param notification_obj: class Notification object
    """
    send_mail(subject=notification_obj.subject, message=notification_obj.message, from_email=EMAIL_HOST_USER,
              recipient_list=[User.objects.get(id=notification_obj.recipient_id).email])


def send_telegram(notification_obj):
    """
    Takes Notification object, calls UserProfile object by Notification object`s recipient id, takes telegram_id attribute from UserProfile object,
    and sends notification text to available telegram id.
    :param notification_obj: class Notification object
    """
    telegram_id = (UserProfile.objects.get(user=notification_obj.recipient)).telegram_id
    bot.send_message(telegram_id, notification_obj.message)


def send_telegram_reply(telegram_reply_message_obj):
    """
    Takes TelegramReplyMessage object, calls TelegramIncomeMessage object (reply to which), takes TelegramIncomeMessage id and sender chat_id,
    and sends available TelegramReplyMessage text to available chat_id with indicated income message id in response to which this reply is.
    :param telegram_reply_message_obj: class TelegramReplyMessage object
    """
    income_message = TelegramIncomeMessage.objects.get(id=telegram_reply_message_obj.reply_to_message.id)
    income_message_id = income_message.message_id
    chat_id = income_message.chat_id
    text = telegram_reply_message_obj.reply_message
    bot.send_message(reply_to_message_id=income_message_id, chat_id=chat_id, text=text)
