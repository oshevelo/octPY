from celery import Celery
from notifications.sender import send_telegram, send_email, send_telegram_reply
from datetime import datetime
from notifications.models import Notification, TelegramReplyMessage

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def send_email_task(n):
    x = Notification.objects.get(id=n)
    send_email(x)
    x.sent_time = datetime.now()
    x.is_sent = True
    x.save()


@app.task
def send_telegram_task(n):
    x = Notification.objects.get(id=n)
    send_telegram(x)
    x.sent_time = datetime.now()
    x.is_sent = True
    x.save()


@app.task
def send_telegram_reply_task(n):
    x = TelegramReplyMessage.objects.get(id=n)
    send_telegram_reply(x)
    x.sent_time = datetime.now()
    x.is_sent = True
    x.save()


send_methods = {
    'email': send_email_task,
    'telegram': send_telegram_task,
    # 'viber': send_viber,
    # 'sms': send_sms,
    # 'site': send_site
}
