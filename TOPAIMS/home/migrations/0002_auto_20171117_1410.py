# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 14:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notes',
            options={'ordering': ('-Timestamp',)},
        ),
    ]
