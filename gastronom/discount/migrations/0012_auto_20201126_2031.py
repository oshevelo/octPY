# Generated by Django 2.2 on 2020-11-26 20:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0011_auto_20201126_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcart',
            name='valid_date_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 24, 20, 31, 43, 533114, tzinfo=utc), verbose_name='Active to'),
        ),
    ]