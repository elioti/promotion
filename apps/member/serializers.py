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


class RecSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    # def validate(self, attrs):
    #     attrs["ip"] = "127.0.0.1"
    #     attrs["prizeName"] = "这是一份随机的礼物"
    #     return attrs
    def get_ip(self, obj):
        return "127.120.110.111"
    def get_prizeName(self, obj):
        return "这是一份超级大礼包啊啊啊"
    class Meta:
        model = Rec
        list_serializer_class = BulkListSerializer
        fields = "__all__"
        # exclude = ["ip", "prizeName"]

