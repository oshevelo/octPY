from django.contrib import admin
from django.contrib.auth.models import User

from .models import UserProfile
from notifications.models import Notification


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone_number', 'telegram_id']

    def create_notifications(self, request, queryset):
        source = input('Specify notification source: ')
        message = input('Type notification message: ')
        send_method = input('Specify send method: ')
        subject = input('Type notification subject: ')
        Notification.create_notifications(source=source, recipient=[User.objects.get(id=user_profile.user.id) for user_profile in queryset],
                                          message=message,
                                          send_method=send_method,
                                          subject=subject)
    actions = [create_notifications]

# здесь надо спросить, как делать инпуты через админку


admin.site.register(UserProfile, UserProfileAdmin)
