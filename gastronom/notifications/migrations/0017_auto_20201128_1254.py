# Generated by Django 2.2 on 2020-11-28 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0016_auto_20201128_1252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegramreplymessage',
            old_name='reply_to_message_id',
            new_name='reply_to_message',
        ),
    ]
