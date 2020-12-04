import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from telegram import Bot
from telegram.ext import Updater, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.utils.request import Request

from notifications.bot import do_echo, contact_callback, reg_handler, FIRST_NAME, LAST_NAME, EMAIL, BIRTH_DATE, GENDER
from notifications.bot import first_name_handler, last_name_handler, email_handler, birth_date_handler, finish_handler


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        request = Request(connect_timeout=0.5, read_timeout=1.0, con_pool_size=8)
        bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)
        updater = Updater(bot=bot, use_context=True)

        conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(reg_handler, pattern='reg', pass_user_data=True), ],
            states={
                FIRST_NAME: [MessageHandler(Filters.all, first_name_handler, pass_user_data=True), ],
                LAST_NAME: [MessageHandler(Filters.all, last_name_handler, pass_user_data=True), ],
                EMAIL: [MessageHandler(Filters.all, email_handler, pass_user_data=True), ],
                BIRTH_DATE: [MessageHandler(Filters.all, birth_date_handler, pass_user_data=True), ],
                GENDER: [MessageHandler(Filters.all, finish_handler, pass_user_data=True), ],
                 },
            fallbacks=[], )
        updater.dispatcher.add_handler(conv_handler)

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        updater.dispatcher.add_handler(MessageHandler(Filters.contact, contact_callback))

        updater.start_polling()
        updater.idle()
