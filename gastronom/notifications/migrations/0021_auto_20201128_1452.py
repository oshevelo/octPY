# Generated by Django 2.2 on 2020-11-28 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0020_auto_20201128_1448'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegramincomemessage',
            old_name='telegramuser_id',
            new_name='telegramuser',
        ),
    ]
