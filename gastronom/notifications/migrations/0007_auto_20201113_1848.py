# Generated by Django 2.2 on 2020-11-13 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_auto_20201113_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(default='message', max_length=200),
        ),
    ]
