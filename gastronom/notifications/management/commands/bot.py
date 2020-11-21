
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater
from telegram.utils.request import Request
from notifications.models import TelegramUser


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'An error has occurred: {e}'
            print(error_message)
            raise e
    return inner()


# @log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    TelegramUser.objects.get_or_create(telegram_id=chat_id,
                                               defaults={'telegram_user_name': update.message.from_user.username})


    reply_text = f'Your ID: {chat_id}\n\n{text}'
    update.message.reply_text(text=reply_text)


class Command(BaseCommand):
    def handle(self, *args, **options):
        request = Request(connect_timeout=0.5, read_timeout=1.0)
        bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)

        print(bot.get_me())

        updater = Updater(bot=bot, use_context=True)
        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()