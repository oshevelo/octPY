import logging
from dateutil.parser import parse
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update, Bot, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from telegram.utils.request import Request

from gastronom.settings import CHAT_ID, EMAIL_HOST_USER
from notifications.models import TelegramUser, TelegramIncomeMessage, TelegramReplyMessage
from user_profile.models import UserProfile


FIRST_NAME, LAST_NAME, EMAIL, BIRTH_DATE, GENDER = range(5)
gender_dict = {'Жінка': 'Female', 'Чоловік': 'Male', 'Ще визначаюсь': 'Not_specified'}

logger = logging.getLogger(__name__)

try:
    request = Request(connect_timeout=1.0, read_timeout=1.0, con_pool_size=8)
    bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)
except:
    request = None
    bot = None


def do_start(update, context):
    """
    Sends to user a button for authorisation
    :param update: Update
    :param context: CallbackContext
    """
    button = KeyboardButton(text='Надати номер телефону', request_contact=True)
    update.message.reply_text(text="Для початку, надайте свій номер телефону", reply_markup=ReplyKeyboardMarkup([[button]],
                              resize_keyboard=True, one_time_keyboard=True))


def contact_callback(update, context):
    """
    Gets from update the information about user (name, phone number, etc.), writes the telegram user to DB,
    update user profile field 'telegram_id' if there is a user with given phone number
    :param update: Update
    :param context: CallbackContext
    """
    username = update.effective_message.chat.username
    contact = update.effective_message.contact
    user_phone = contact.phone_number[-12:]
    chat_id = contact.user_id
    user_first_name = contact.first_name
    user_last_name = contact.last_name
    TelegramUser.objects.update_or_create(chat_id=chat_id, defaults={'user_first_name': user_first_name, 'user_last_name': user_last_name,
                                                                     'username': username, 'user_phone': user_phone})
    is_user_profile(chat_id, user_phone, update, context)


def is_user_profile(chat_id, user_phone, update, context):
    try:
        user_profile = UserProfile.objects.get(phone_number=user_phone)
        user_profile.telegram_id = chat_id
        user_profile.save(update_fields=['telegram_id'], force_update=True)
    except Exception as e:
        logger.info(e)
        bot.send_message(CHAT_ID, text=f'{e}')
        registration(update, context)


def registration(update, context):
    button = [[InlineKeyboardButton(text='Зареєструватись', callback_data='reg')]]
    update.message.reply_text(text='Ви не є покупцем гастроному, але це поки що', reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(text='Будь ласка, пройдіть реєстрацію!', reply_markup=InlineKeyboardMarkup(button))


def do_echo(update, context):
    """
    Makes object 'income message' in DB.
    :param update: Update
    :return:
    """
    chat_id = update.message.chat.id  # chat_id from income message
    text = update.message.text  # income message text

    if chat_id == CHAT_ID:  # if message came from me
        reply = update.message.reply_to_message  # to which message this my reply
        t = TelegramReplyMessage(reply_to_message=list(TelegramIncomeMessage.objects.filter(text=reply.text))[-1], reply_message=text)
        if reply.forward_from is None:
            first_name = reply.forward_sender_name.split(' ')[0]
            last_name = reply.forward_sender_name.split(' ')[1]
            bot.send_message(chat_id=TelegramUser.objects.get(user_first_name=first_name, user_last_name=last_name).chat_id, text=text)
            t.is_sent = True
            t.sent_time = datetime.now()
            t.save()
        else:
            bot.send_message(chat_id=reply.forward_from.id, text=text)  # forward my reply to user
            t.is_sent = True
            t.sent_time = datetime.now()
            t.save()

    else:
        message_id = update.message.message_id
        bot.forward_message(chat_id=CHAT_ID, from_chat_id=chat_id, message_id=message_id)
        t, _ = TelegramUser.objects.update_or_create(chat_id=chat_id, defaults={'chat_id': chat_id, 'username': update.message.from_user.username,
                                                                                'user_first_name': update.message.from_user.first_name,
                                                                                'user_last_name': update.message.from_user.last_name})
        TelegramIncomeMessage(telegramuser=t, text=text, message_id=message_id, chat_id=chat_id, date=update.message.date).save()
        user_phone = str
        try:
            user_phone = TelegramUser.objects.get(chat_id=chat_id).user_phone
        except Exception as e:
            bot.send_message(CHAT_ID, text=f'{e}')
            logger.info(e)
            return do_start(update, context)

        if text == '/start' or user_phone is None or user_phone == '':
            return do_start(update, context)

        is_user_profile(chat_id, user_phone, update, context)


def reg_handler(update: Update, context: CallbackContext):
    update.effective_message.reply_text("Вкажіть Ваше ім`я:")
    return FIRST_NAME


def first_name_handler(update: Update, context: CallbackContext):
    context.user_data[FIRST_NAME] = update.effective_message.text
    update.effective_message.reply_text(f'Дякую, {context.user_data[FIRST_NAME]}, тепер вкажіть Ваше прізвище:')
    return LAST_NAME


def last_name_handler(update, context):
    context.user_data[LAST_NAME] = update.effective_message.text
    update.effective_message.reply_text(f'Надрукуйте будь ласка свій e-mail')
    return EMAIL


def email_handler(update, context):
    context.user_data[EMAIL] = update.effective_message.text
    try:
        send_mail(subject='GASTRONOM registration', message='Ви в процесі реєстрації, по всім питанням пишіть нам у Telegram @GASTRONOM_django_bot',
                  from_email=EMAIL_HOST_USER, recipient_list=[context.user_data[EMAIL]])
    except Exception as e:
        logger.info(e)
        update.effective_message.reply_text(f'Ви надрукували неправильний e-mail, спробуйте ще раз!')
        bot.send_message(CHAT_ID, text=f'{e}')
        return LAST_NAME
    update.effective_message.reply_text(f'Дата Вашого народження: дд-мм-рррр')
    return BIRTH_DATE


def birth_date_handler(update: Update, context: CallbackContext):
    context.user_data[BIRTH_DATE] = update.effective_message.text
    try:
        parse(str(context.user_data[BIRTH_DATE]), dayfirst=True)
    except Exception as e:
        logger.info(e)
        update.effective_message.reply_text(f'Неправильний формат дати, спробуйте ще раз!')
        bot.send_message(CHAT_ID, text=f'{e}')
        return BIRTH_DATE
    gender_keys = [['Жінка'], ['Чоловік'], ['Ще визначаюсь']]
    update.effective_message.reply_text(text='Це останнє, вкажіть Вашу стать:', reply_markup=ReplyKeyboardMarkup(gender_keys, one_time_keyboard=True))
    return GENDER


def finish_handler(update: Update, context: CallbackContext):
    gender = update.effective_message.text
    context.user_data[GENDER] = gender_dict[gender]
    try:
        u, _ = User.objects.update_or_create(email=context.user_data[EMAIL],
                                             defaults={'first_name': context.user_data[FIRST_NAME],
                                                       'last_name': context.user_data[LAST_NAME],
                                                       'username': f'{context.user_data[FIRST_NAME][0]} {context.user_data[LAST_NAME][0]}'
                                                                   f' {context.user_data[EMAIL]}'})
        UserProfile.objects.update_or_create(user=u,
                                             defaults={'first_name': u.first_name, 'last_name': u.last_name,
                                                       'phone_number': TelegramUser.objects.get(chat_id=update.effective_message.chat_id).user_phone,
                                                       'email': u.email, 'telegram_id': update.effective_message.chat_id,
                                                       'birth_date': parse(context.user_data[BIRTH_DATE]), 'gender': context.user_data[GENDER]})
        update.effective_message.reply_text(text=f'Вітаю! Реєстрація успішна!\nВи можете друкувати повідомлення та отримувати новини Гастроному',
                                            reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        logger.info(e)
        update.effective_message.reply_text(f'Під час реєстрації виникла помилка але ми це виправимо!', reply_markup=ReplyKeyboardRemove())
        bot.send_message(CHAT_ID, text=f'{e}')
    return ConversationHandler.END
