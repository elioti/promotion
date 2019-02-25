#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: June
# @Time : 2019/2/21
from rest_framework import serializers
from member.models import Rec
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)
from rest_framework_extensions import bulk_operations


class RecSerializer(serializers.ModelSerializer):
    # def validate(self, attrs):
    #     attrs["ip"] = "127.0.0.1"
    #     attrs["prizeName"] = "这是一份随机的礼物"
    #     return attrs
    class Meta:
        model = Rec
        # list_serializer_class = BulkListSerializer  # 当需要使用Bulk update时使用
        fields = "__all__"
        # exclude = ["ip", "prizeName"]
        extra_kwargs = {'ip': {'read_only': True}, 'prizeName': {'read_only': True}}
