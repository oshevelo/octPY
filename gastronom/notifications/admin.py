from django.contrib import admin

from .models import Notification, TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    model = TelegramUser
    list_display = ('id', 'telegram_id', 'telegram_user_name')


class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 1


admin.site.register(Notification)
