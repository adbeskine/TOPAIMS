# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-14 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20171114_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='Job',
        ),
        migrations.AddField(
            model_name='jobs',
            name='notes',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='home.Notes'),
        ),
    ]