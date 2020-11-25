import logging
from django.core.mail import send_mail
from gastronom.settings import EMAIL_HOST_USER

logger = logging.getLogger('__name__')


def send_method_validator(send_method):
    send_methods = {
        'email': send_email,
        # 'telegram': send_telegram,
        # 'viber': send_viber,
        # 'sms': send_sms,
        # 'site': send_site,
    }
    try:
        send_func = send_methods[send_method]
        return send_func
    except KeyError as send_method_error:
        logger.error(f'unsupported send_method! {send_method_error}')


def send_email(recipient_email, message):
    recipient_email = [recipient_email]
    send_mail(subject='GASTRONOM info', message=message, from_email=EMAIL_HOST_USER, recipient_list=recipient_email)

