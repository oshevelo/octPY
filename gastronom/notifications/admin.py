from django.contrib import admin

from .models import Notification



class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 1


admin.site.register(Notification)
