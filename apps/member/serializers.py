#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: June
# @Time : 2019/2/21
from rest_framework import serializers
from member.models import Rec


class RecSerializer(serializers.ModelSerializer):
    # def validate(self, attrs):
    #     attrs["ip"] = "127.0.0.1"
    #     attrs["prizeName"] = "这是一份随机的礼物"
    #     return attrs

    class Meta:
        model = Rec
        fields = "__all__"
