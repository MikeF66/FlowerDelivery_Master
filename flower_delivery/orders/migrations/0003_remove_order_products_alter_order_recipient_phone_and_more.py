# Generated by Django 5.0.7 on 2024-08-08 21:55

import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AlterField(
            model_name='order',
            name='recipient_phone',
            field=models.CharField(max_length=25, verbose_name='Телефон получателя'),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=jsonfield.fields.JSONField(default='', verbose_name='Товары'),
            preserve_default=False,
        ),
    ]
