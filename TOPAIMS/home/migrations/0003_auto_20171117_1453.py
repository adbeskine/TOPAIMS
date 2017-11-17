# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20171117_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='status',
            field=models.CharField(default='quote', max_length=100),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='job_id',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
