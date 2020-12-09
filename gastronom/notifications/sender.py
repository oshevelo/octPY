import logging
from datetime import datetime
from celery import app

from django.core.mail import send_mail
from django.conf import settings

from telegram import Bot
from telegram.utils.request import Request

from gastronom.settings import EMAIL_HOST_USER
from user_profile.models import UserProfile


logger = logging.getLogger(__name__)


@app.shared_task
def send_email(n):
    send_mail(subject=n.subject, message=n.message, from_email=EMAIL_HOST_USER, recipient_list=[n.recipient.email])
    n.sent_time = datetime.now()
    n.is_sent = True
    n.save()


@app.shared_task
def send_telegram(n):
    recipient = UserProfile.objects.get(user=n.recipient)
    telegram_id = recipient.telegram_id
    request = Request(connect_timeout=1, read_timeout=1.0, con_pool_size=8)
    bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)
    bot.send_message(telegram_id, n.message)
    n.sent_time = datetime.now()
    n.is_sent = True
    n.save()


send_methods = {
    'email': send_email,
    'telegram': send_telegram,
    # 'viber': send_viber,
    # 'sms': send_sms,
    # 'site': send_site
}
