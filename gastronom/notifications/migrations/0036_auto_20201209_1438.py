# Generated by Django 2.2 on 2020-12-09 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0035_auto_20201205_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='sent',
            new_name='is_sent',
        ),
        migrations.AddField(
            model_name='notification',
            name='sent_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
