from django.contrib import admin

from .models import Notification, TelegramUser, TelegramIncomeMessage


class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 1


class TelegramIncomeMessageInline(admin.TabularInline):
    model = TelegramIncomeMessage


class TelegramUserAdmin(admin.ModelAdmin):
    inlines = [TelegramIncomeMessageInline]
    list_display = ('id', 'telegram_id', 'telegram_user_name', 'telegram_user_phone')


admin.site.register(Notification)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramIncomeMessage)
