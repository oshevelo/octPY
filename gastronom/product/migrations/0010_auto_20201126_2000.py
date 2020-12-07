# Generated by Django 2.2 on 2020-11-26 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20201126_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmedia',
            name='large_image',
            field=models.ImageField(editable=False, null=True, upload_to='products/%Y/%m/%d/larges/'),
        ),
        migrations.AlterField(
            model_name='characteristic',
            name='descriptions',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='descriptions',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='productmedia',
            name='image',
            field=models.ImageField(null=True, upload_to='products/%Y/%m/%d/originals/'),
        ),
    ]