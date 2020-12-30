import logging

from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
# from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin
from gastronom.settings import USE_QUEUE
from notifications.models import Notification, TelegramUser, TelegramIncomeMessage, TelegramReplyMessage
from notifications.tasks import send_methods, send_telegram_reply_task


logger = logging.getLogger(__name__)


class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('id', 'is_sent', 'sent_time', 'source', 'recipient', 'send_method', 'timestamp', 'subject', 'message')
    extra = 1
    # list_display_links = ['recipient']
    list_filter = ['is_sent', 'source', 'recipient', 'send_method', 'subject']
    autocomplete_fields = ['recipient']

    def send_notifications(self, request, queryset):
        for notification in queryset:
            send_func = send_methods[notification.send_method]
            if USE_QUEUE:
                send_func.delay(notification.id)
            else:
                send_func(notification.id)

    def make_unsent(self, request, queryset):
        for notification in queryset:
            notification.sent = False
            notification.save()

    actions = [send_notifications, make_unsent]


def send_reply(TelegramReplyMessageInlineAdmin, request, queryset):
    for reply_message in queryset:
        if USE_QUEUE:
            send_telegram_reply_task.delay(reply_message.id)
        else:
            send_telegram_reply_task(reply_message.id)


class TelegramReplyMessageInlineAdmin(admin.StackedInline): #SuperInlineModelAdmin):
    model = TelegramReplyMessage
    list_display = ('id', 'reply_message', 'reply_to_message')
    extra = 1
    actions = [send_reply]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 100})},
    }


class TelegramReplyMessageAdmin(admin.ModelAdmin):
    model = TelegramReplyMessage
    list_display = ('id', 'is_sent', 'sent_time', 'reply_message', 'reply_to_message')
    actions = [send_reply]
    extra = 1


class TelegramIncomeMessageInlineAdmin(admin.StackedInline): # SuperInlineModelAdmin):
    model = TelegramIncomeMessage
    extra = 1
    list_display = ('telegramuser', 'id', 'date', 'message_id', 'chat_id', 'text')
    fields = ['telegramuser', 'text']
    inlines = (TelegramReplyMessageInlineAdmin,)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 100})},
    }


class TelegramIncomeMessageAdmin(admin.ModelAdmin):
    model = TelegramIncomeMessage
    inlines = [TelegramReplyMessageInlineAdmin]
    list_display = ('telegramuser', 'text', 'id', 'date', 'message_id', 'chat_id')


class TelegramUserAdmin(admin.ModelAdmin):
    model = TelegramUser
    list_display = ('id', 'chat_id', 'username', 'user_phone')
    inlines = [TelegramIncomeMessageInlineAdmin]
    list_display_links = ('chat_id', 'username', 'user_phone')
    extra = 1
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 30})},
        }


admin.site.register(Notification, NotificationAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramIncomeMessage, TelegramIncomeMessageAdmin)
admin.site.register(TelegramReplyMessage, TelegramReplyMessageAdmin)
