from django.contrib import admin
from notifications.models import Notification, TelegramUser, TelegramIncomeMessage, TelegramReplyMessage
from telegram import Bot
from telegram.utils.request import Request
from django.conf import settings


class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('id', 'source', 'recipient', 'send_method', 'timestamp', 'subject', 'message')
    extra = 1


def send_reply(TelegramReplyMessageInline, request, queryset):
    bot = Bot(request=Request(connect_timeout=0.5, read_timeout=1.0, con_pool_size=8), token=settings.TOKEN,
              base_url=settings.PROXY_URL)
    for reply_message in queryset:
        income_message = TelegramIncomeMessage.objects.get(id=reply_message.reply_to_message.id)
        income_message_id = income_message.message_id
        chat_id = income_message.chat_id
        text = reply_message.reply_message
        bot.send_message(reply_to_message_id=income_message_id, chat_id=chat_id, text=text)


class TelegramReplyMessageInline(admin.TabularInline):
    model = TelegramReplyMessage
    list_display = ('id', 'reply_message', 'reply_to_message')
    # actions = [send_reply]
    extra = 1


class TelegramReplyMessageAdmin(admin.ModelAdmin):
    model = TelegramReplyMessage
    list_display = ('id', 'reply_to_message', 'reply_message')
    actions = [send_reply]
    extra = 1


class TelegramIncomeMessageAdmin(admin.ModelAdmin):
    model = TelegramIncomeMessage
    inlines = [TelegramReplyMessageInline]
    list_display = ('telegramuser', 'text', 'id', 'created_at', 'message_id', 'chat_id')


class TelegramIncomeMessageInline(admin.TabularInline):
    model = TelegramIncomeMessage
    extra = 1
    list_display = ('telegramuser', 'text', 'id', 'created_at', 'message_id', 'chat_id')


class TelegramUserAdmin(admin.ModelAdmin):
    model = TelegramUser
    list_display = ('id', 'chat_id', 'telegram_user_name', 'telegram_user_phone')
    inlines = [TelegramIncomeMessageInline]
    extra = 1


admin.site.register(Notification, NotificationAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramIncomeMessage, TelegramIncomeMessageAdmin)
admin.site.register(TelegramReplyMessage, TelegramReplyMessageAdmin)

