from django.shortcuts import render
from django.http.response import JsonResponse
import bisect, random, datetime, pytz
from member.serializers import RecSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from member.models import Rec, Member
from item.models import Rule, Info
from
from django_filters import rest_framework as filters
from rest_framework import filters
from django_filters import rest_framework
from utils.views import GoodsPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework_extensions.mixins import ListUpdateModelMixin
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)

# Create your views here.


class RecViewSet(viewsets.ModelViewSet):
    """
    list:
    create:
    update:
    delete:
    """
    # permission_classes = (IsAuthenticated, )
    serializer_class = RecSerializer
    queryset = Rec.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ('user', 'id')
    ordering_fields = ('user', 'id')
    # pagination_class = GoodsPagination
    def list(self, request, *args, **kwargs):
        print(self.request)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print(serializer.data)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     # serializer = self.get_serializer(data=data)
    #     # serializer.is_valid(raise_exception=True)
    #     # self.perform_create(serializer)
    #     bulk = isinstance(request.data, list)
    #     if not bulk:
    #         request.data = data
    #         return super(RecViewSet, self).create(request, *args, **kwargs)
    #
    #     else:
    #         serializer = self.get_serializer(data=request.data, many=True)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_bulk_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def get_serializer(self, *args, **kwargs):
    #     # kwargs['context'] = {'request': self.request}
    #     if isinstance(kwargs.get('data', {}), list):
    #         kwargs['many'] = True
    #     return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        if 'HTTP_X_FORWARDED_FOR' in self.request.META.values():
            ip = self.request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = self.request.META['REMOTE_ADDR']
        if self.request.user.is_staff:
            serializer.save(ip=ip, prizeName='哈哈哈哈或或或')
        else:
            # 抽奖代码
            info = Info.objects.last()
            if info is None:
                return JsonResponse({'code':1, 'error':'请联系网站管理员，初始活动信息'})
            now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))
            if now < info.start_time or now > info.end_time:
                return JsonResponse({'code':2, 'error':'不在活动时间内','message':info.errmsg})
            user = serializer.data['user']
            try:
                member = Member.objects.get(username=user)
            except Member.DoesNotExist:
                return JsonResponse({'code':3,'error':'账号不满足活动要求'})
            # 判断是否有次数
            if member.score < 1:
                return JsonResponse({'code':4,'error':'账号已没有活动次数'})
            try:
                # 判断是否有内定规则
                rule = Rule.objects.get(user=self.request.user)
                code = rule.get_order()
                if code is None:
                    raise Rule.DoesNotExist
            except Rule.DoesNotExist:
                # 自然抽奖
                pass
            else:
                serializer.save(
                    ip=ip,
                    prizeName='内定的礼品',
                    prizeId=code,
                    type=1,
                )
                rule.flag = rule.flag+1




