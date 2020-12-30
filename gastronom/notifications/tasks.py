from celery import Celery
from notifications.sender import send_telegram, send_email, send_telegram_reply
from django.utils import timezone
from notifications.models import Notification, TelegramReplyMessage

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def send_email_task(notification_id):
    """
    Calls Notification object by notification_id from DB, put Notification object to called function "send_email", changes attribute is_sent to True
    and attribute sent_time to timezone.now.
    :param notification_id: int
    """
    notification_obj = Notification.objects.get(id=notification_id)
    send_email(notification_obj)
    notification_obj.sent_time = timezone.now()
    notification_obj.is_sent = True
    notification_obj.save()


@app.task
def send_telegram_task(notification_id):
    """
    Calls Notification object by notification_id from DB, put Notification object to called function "send_telegram", changes attribute is_sent to
    True and attribute sent_time to timezone.now.
    :param notification_id: int
    """
    notification_obj = Notification.objects.get(id=notification_id)
    try:
        send_telegram(notification_obj)
        notification_obj.sent_time = timezone.now()
        notification_obj.is_sent = True
        notification_obj.save()
    except Exception as e:
        send_email_task(notification_id)


@app.task
def send_telegram_reply_task(telegram_reply_message_id):
    """
    Calls TelegramReplyMessage object by telegram_reply_message_id from DB, put TelegramReplyMessage object to a called function "send_telegram_reply",
    changes attribute is_sent to True and attribute sent_time to timezone.now.
    :param telegram_reply_message_id: int
    """
    telegram_reply_message_obj = TelegramReplyMessage.objects.get(id=telegram_reply_message_id)
    send_telegram_reply(telegram_reply_message_obj)
    telegram_reply_message_obj.sent_time = timezone.now()
    telegram_reply_message_obj.is_sent = True
    telegram_reply_message_obj.save()


send_methods = {
    'email': send_email_task,
    'telegram': send_telegram_task,
    # 'viber': send_viber,
    # 'sms': send_sms,
    # 'site': send_site
}
