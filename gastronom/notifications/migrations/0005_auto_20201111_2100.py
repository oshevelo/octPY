# Generated by Django 2.2 on 2020-11-11 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0004_auto_20201110_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='source',
            field=models.CharField(choices=[('jet', 'jet'), ('comments.apps.CommentsConfig', 'comments.apps.CommentsConfig'), ('notifications', 'notifications'), ('catalog', 'catalog'), ('django.contrib.admin', 'django.contrib.admin'), ('django.contrib.auth', 'django.contrib.auth'), ('django.contrib.contenttypes', 'django.contrib.contenttypes'), ('django.contrib.sessions', 'django.contrib.sessions'), ('django.contrib.messages', 'django.contrib.messages'), ('django.contrib.staticfiles', 'django.contrib.staticfiles'), ('cart', 'cart')], max_length=200),
        ),
    ]