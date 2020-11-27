from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram import Update, Bot
from telegram.ext import CallbackContext
from telegram.utils.request import Request

from django.conf import settings

from notifications.models import TelegramUser, TelegramIncomeMessage
from user_profile.models import UserProfile

request = Request(connect_timeout=0.5, read_timeout=1.0, con_pool_size=8)
bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)


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
    button = KeyboardButton(text='Авторизуватись', request_contact=True)
    update.message.reply_text(text="Без авторизації розмови не буде",
                              reply_markup=ReplyKeyboardMarkup([[button]],
                                                               resize_keyboard=True, one_time_keyboard=True))


def contact_callback(update: Update, context: CallbackContext):
    chat_id = update.effective_message.contact.user_id
    contact = update.effective_message.contact
    phone = contact.phone_number[-12:]
    TelegramUser.objects.update_or_create(chat_id=chat_id, defaults={'telegram_user_phone': phone})
    try:
        UserProfile.objects.update_or_create(phone_number=phone, defaults={'telegram_id': chat_id})
    except Exception as e:
        bot.send_message(chat_id=chat_id, text='Ви не є покупцем гастроному')


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    text = update.message.text
    p, _ = TelegramUser.objects.update_or_create(chat_id=chat_id,
                                                 defaults={'telegram_user_name': update.message.from_user.username})
    TelegramIncomeMessage(telegramuser=p, text=text).save()
    telegram_user_phone = TelegramUser.objects.get(chat_id=chat_id).telegram_user_phone
    bot.send_message(chat_id=403274033, text=f'{chat_id}: username: {update.message.from_user.username}'
                                             f' text: {text} phone_number: {telegram_user_phone}')
    if text == '/start':
        return do_start(update)
    else:
        if telegram_user_phone is None or telegram_user_phone == '':
            return do_start(update)
        else:
            try:
                UserProfile.objects.update_or_create(phone_number=telegram_user_phone,
                                                     defaults={'telegram_id': chat_id})
                bot.send_message(chat_id=chat_id, text='Відповідач у розробці, він з Вами зв`яжеться трішки пізніше')
            except Exception as e:
                bot.send_message(chat_id=chat_id, text='Кажу ж, Ви не є покупцем гастроному')
