# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-22 06:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_siteadmin_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='day_end',
            field=models.TimeField(default=None, null=True, verbose_name='日结'),
        ),
        migrations.AddField(
            model_name='info',
            name='day_start',
            field=models.TimeField(default=None, null=True, verbose_name='日启'),
        ),
    ]
