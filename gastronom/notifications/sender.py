from django.core.mail import send_mail
from gastronom.settings import EMAIL_HOST_USER
from telegram import Bot
from telegram.utils.request import Request
from django.conf import settings
from user_profile.models import UserProfile


def send_email(recipient, message):
    recipient = [recipient.email]
    send_mail(subject='GASTRONOM info', message=message, from_email=EMAIL_HOST_USER, recipient_list=recipient)


def send_telegram(recipient, message):

    recipient = UserProfile.objects.get(user=recipient)
    telegram_id = recipient.telegram_id
    request = Request(connect_timeout=0.5, read_timeout=1.0, con_pool_size=8)
    bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)
    bot.send_message(telegram_id, message)


send_methods = {
    'email': send_email,
    'telegram': send_telegram,
    # 'viber': send_viber,
    # 'sms': send_sms,
    # 'site': send_site
}
