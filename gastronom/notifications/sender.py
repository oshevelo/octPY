import logging

from django.core.mail import send_mail
from django.contrib.auth.models import User

from gastronom.settings import EMAIL_HOST_USER
from user_profile.models import UserProfile
from notifications.models import TelegramIncomeMessage
from notifications.bot import bot


logger = logging.getLogger(__name__)


def send_email(x):
    send_mail(subject=x.subject, message=x.message, from_email=EMAIL_HOST_USER, recipient_list=[User.objects.get(id=x.recipient_id).email])


def send_telegram(x):
    telegram_id = (UserProfile.objects.get(user=x.recipient)).telegram_id
    bot.send_message(telegram_id, x.message)


def send_telegram_reply(x):
    income_message = TelegramIncomeMessage.objects.get(id=x.reply_to_message.id)
    income_message_id = income_message.message_id
    chat_id = income_message.chat_id
    text = x.reply_message
    bot.send_message(reply_to_message_id=income_message_id, chat_id=chat_id, text=text)
