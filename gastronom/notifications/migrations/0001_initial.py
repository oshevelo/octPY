# Generated by Django 2.2 on 2020-11-09 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=20)),
                ('send_method', models.CharField(choices=[('email', 'E-mail'), ('messenger', 'Messenger'), ('site', 'Site')], default='e-mail', max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('verb', models.CharField(max_length=200)),
                ('recipient', models.ForeignKey(on_delete=models.SET('user_id'), to='user_profile.User')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
    ]