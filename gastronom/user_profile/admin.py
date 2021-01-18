from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

from notifications.views import create_notifications
from .models import UserProfile
from notifications.models import Notification


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone_number', 'telegram_id']

    def create_notifications(NotificationAdmin, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = CreateNotificationsForm(request.POST)
            if form.is_valid():
                send_method = form.cleaned_data['send_method']
                subject = form.cleaned_data['subject']
                text = form.cleaned_data['text']
                source = form.cleaned_data['source']
                count = 0
                for user_profile in queryset:
                    create_notifications(source=source, recipients=[User.objects.get(id=user_profile.user.id)], message=text,
                                          send_method=send_method,
                                         subject=subject)
                    count += 1
                NotificationAdmin.message_user(request, f'Notifications was created and sent to {count} users')
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = CreateNotificationsForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render(request, 'user_profile/templates/create_notifications.html', {'items': queryset, 'form': form, 'title': u'Create notifications'})
    create_notifications.short_description = u"Create notifications"

    actions = [create_notifications]


class CreateNotificationsForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    subject = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    source = forms.ChoiceField(widget=forms.RadioSelect, choices=Notification.SOURCE)
    send_method = forms.ChoiceField(widget=forms.RadioSelect, choices=Notification.send_methods)


admin.site.register(UserProfile, UserProfileAdmin)
