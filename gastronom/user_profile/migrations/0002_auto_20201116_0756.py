# Generated by Django 2.2 on 2020-11-16 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.IntegerField(choices=[('Male', 'Male'), ('Female', 'Female'), ('not specified', 'not specified')], default='not specified'),
        ),
    ]
