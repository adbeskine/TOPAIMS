# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 06:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduled_items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=1)),
                ('date1', models.DateField(default=datetime.date(2017, 11, 22))),
                ('date2', models.DateField(default=models.DateField(default=datetime.date(2017, 11, 22)))),
                ('quantity', models.IntegerField(default=1)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Jobs')),
            ],
        ),
    ]
