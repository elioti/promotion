# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-19 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20190320_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rec',
            name='prizeId',
            field=models.IntegerField(default=None, null=True, verbose_name='奖品ID'),
        ),
    ]