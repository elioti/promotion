#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: June
# @Time : 2019/2/18
from rest_framework import serializers
from item.models import Prize, Rule, Info


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = "__all__"


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = "__all__"


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = "__all__"
