#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: June
# @Time : 2019/2/22
from django.contrib.auth import get_user_model
from rest_framework import serializers


class AdminSerializer(serializers.ModelSerializer):
    # def validate(self, attrs):
    #     attrs["ip"] = "127.0.0.1"
    #     attrs["prizeName"] = "这是一份随机的礼物"
    #     return attrs

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "is_superuser", "last_login")
