# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20171129_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_orders',
            name='order_no',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
