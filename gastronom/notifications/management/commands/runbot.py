from django.conf import settings
from django.core.management.base import BaseCommand

from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater
from telegram.utils.request import Request

from notifications.bot import do_echo, contact_callback


class Command(BaseCommand):
    def handle(self, *args, **options):
        request = Request(connect_timeout=0.5, read_timeout=1.0, con_pool_size=8)
        bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)
        updater = Updater(bot=bot, use_context=True)

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        updater.dispatcher.add_handler(MessageHandler(Filters.contact, contact_callback))
        updater.start_polling()
        updater.idle()
