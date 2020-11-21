# import smtplib
# import ssl
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
# from telegram.client import Telegram
import logging
from django.core.mail import send_mail
from gastronom.settings import EMAIL_HOST_USER
from telethon import TelegramClient, events, sync
# from telegram.client import Telegram


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


# bot = telebot.TeleBot('1207335127:AAFk-8mBpTpNZhuuAmkJ7oAIAPPDGrXM71o')
#
#
#
#
# api_id = 2491082
# api_hash = 'a0c5768298ed27690afef179a7f380f1'
# chat_id = -1001401749218
# text = 'my message text'
# bot_token = '1207335127:AAFk-8mBpTpNZhuuAmkJ7oAIAPPDGrXM71o'
#
# client = TelegramClient('session_name', api_id, api_hash)
# client.start()
#
# tg = Telegram(
#     api_id=api_id,
#     api_hash=api_hash,
#     phone='-1001401749218',  # you can pass 'bot_token' instead
#     database_encryption_key='database_encryption_key',
# )
# tg.login()
#
# # if this is the first run, library needs to preload all chats
# # otherwise the message will not be sent
# result = tg.get_chats()
# result.wait()
#
# result = tg.send_message(
#     chat_id=chat_id,
#     text=text,
# )
# # `tdlib` is asynchronous, so `python-telegram` always returns you an `AsyncResult` object.
# # You can receive a result with the `wait` method of this object.
# result.wait()
# print(result.update)
#
# tg.stop()  # you must call `stop` at the end of the script
#
# #
# # phone = '+380972302031'
