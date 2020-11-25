from django.conf import settings
from django.core.management.base import BaseCommand

from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater
from telegram.utils.request import Request

from notifications.models import TelegramUser, TelegramIncomeMessage


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'An error has occurred: {e}'
            print(error_message)
            raise e
    return inner


def do_start(update):
    button = KeyboardButton(text='Надати мій номер телефону', request_contact=True)
    update.message.reply_text(text="Чи Ви згодні надати свій номер телефону?",
                              reply_markup=ReplyKeyboardMarkup([[button]], resize_keyboard=True,
                                                               one_time_keyboard=True))
    update.message.reply_text(f'{update.message.contact.phone_number}')


def contact_callback(update: Update, context: CallbackContext):
    chat_id = update.effective_message.contact.user_id
    contact = update.effective_message.contact
    phone = contact.phone_number
    TelegramUser.objects.update_or_create(telegram_id=chat_id, defaults={'telegram_user_phone': phone})
    # TelegramUser.objects.update_or_create(telegram_user_phone=phone,
    #                                       defaults={'telegram_user': UserProfile.objects.get(phone_number=phone)})


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    text = update.message.text
    p, _ = TelegramUser.objects.update_or_create(telegram_id=chat_id,
                                                 defaults={'telegram_user_name': update.message.from_user.username})
    TelegramIncomeMessage(telegramuser=p, text=text).save()
    if text == '/start':
        return do_start(update)


class Command(BaseCommand):
    def handle(self, *args, **options):
        request = Request(connect_timeout=0.5, read_timeout=1.0)
        bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)
        updater = Updater(bot=bot, use_context=True)

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        updater.dispatcher.add_handler(MessageHandler(Filters.contact, contact_callback))
        updater.start_polling()
        updater.idle()
