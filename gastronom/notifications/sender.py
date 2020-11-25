from django.core.mail import send_mail
from gastronom.settings import EMAIL_HOST_USER


def send_email(recipient_email, message):
    recipient_email = [recipient_email]
    send_mail(subject='GASTRONOM info', message=message, from_email=EMAIL_HOST_USER, recipient_list=recipient_email)


send_methods = {
    'email': send_email,
    # 'telegram': send_telegram,
    # 'viber': send_viber,
    # 'sms': send_sms,
    # 'site': send_site,
    }
