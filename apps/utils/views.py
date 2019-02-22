#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: June
# @Time : 2019/2/19
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.contrib.auth import authenticate, login
from rest_framework import serializers
from django.utils.translation import ugettext as _
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


class CustomAuthSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        print(attrs, 'attrs')
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
                return {
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class ObtainSessionWebToken(JSONWebTokenAPIView):
    serializer_class = CustomAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user')
            login(request, user)
            response_data = {
                'code': 200
            }
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    page_query_param = "page"
    max_page_size = 50