# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-18 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='会员账号')),
                ('score', models.IntegerField(default=0, verbose_name='活动次数')),
            ],
        ),
        migrations.CreateModel(
            name='Rec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32, verbose_name='活动用户')),
                ('prize_name', models.CharField(max_length=64, verbose_name='奖品名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('send_time', models.DateTimeField(default=None, null=True, verbose_name='发送时间')),
                ('is_sent', models.BooleanField(default=False, verbose_name='是否发送')),
                ('user_ip', models.GenericIPAddressField(verbose_name='抽奖IP')),
                ('way', models.CharField(default='自然抽奖', max_length=100, verbose_name='抽奖方式')),
            ],
            options={
                'verbose_name': '活动记录',
                'verbose_name_plural': '活动记录',
            },
        ),
    ]
