# Generated by Django 2.2 on 2020-12-14 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0039_merge_20201213_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='source',
            field=models.CharField(choices=[('activity', 'activity'), ('analytics', 'analytics'), ('cart', 'cart'), ('catalog', 'catalog'), ('comments', 'comments'), ('discount', 'discount'), ('info', 'info'), ('loyalty', 'loyalty'), ('notifications', 'notifications'), ('order', 'order'), ('payment', 'payment'), ('product', 'product'), ('shipment', 'shipment'), ('user_profile', 'user_profile'), ('other_source', 'other_source')], max_length=200),
        ),
        migrations.AlterField(
            model_name='telegramincomemessage',
            name='text',
            field=models.TextField(max_length=200, verbose_name='Income message'),
        ),
    ]