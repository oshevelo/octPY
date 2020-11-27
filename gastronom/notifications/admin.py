from django.contrib import admin
from .models import Notification, TelegramUser, TelegramIncomeMessage, TelegramReplyMessage


class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 1


class TelegramIncomeMessageInline(admin.TabularInline):
    model = TelegramIncomeMessage


class TelegramUserAdmin(admin.ModelAdmin):
    inlines = [TelegramIncomeMessageInline]
    list_display = ('id', 'telegram_id', 'telegram_user_name', 'telegram_user_phone')


class TelegramReplyMessageAdminInline(admin.StackedInline):
    model = TelegramReplyMessage
    list_display = ('id', 'reply_to', 'reply_message')


admin.site.register(Notification)
admin.site.register(TelegramUser)
admin.site.register(TelegramIncomeMessage)
admin.site.register(TelegramReplyMessage)

