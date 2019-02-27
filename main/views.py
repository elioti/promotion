from .serializers import AdminSerializer, PrizeSerializer, RuleSerializer, RecSerializer, MemberRecSerializer, InfoSerializer
from rest_framework import viewsets
from .models import *
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, authentication
import bisect
import random
import datetime
import pytz
# Create your views here.


class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdminSerializer
    queryset = SiteAdmin.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ('username', 'id')
    ordering_fields = ('username', 'id')


class PrizeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ('prize_name', 'id')
    ordering_fields = ('prize_name', 'id')


class RuleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ('user', 'id')
    ordering_fields = ('id',)


class InfoViewSet(viewsets.ModelViewSet):
    serializer_class = InfoSerializer
    queryset = Info.objects.all()


class RecViewSet(viewsets.ModelViewSet):
    serializer_class = RecSerializer
    queryset = Rec.objects.get_queryset().order_by('id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ('user', 'id')
    ordering_fields = ('id',)

    def get_permissions(self):
        pass

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return RecSerializer
        else:
            return MemberRecSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'HTTP_X_FORWARDED_FOR' in self.request.META.values():
            ip = self.request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = self.request.META['REMOTE_ADDR']
        prizes = Prize.objects.all()
        if self.request.user.is_staff:
            prize = prizes.get(code=serializer.validated_data['code'])
            serializer.save(ip=ip, prizeName=prize.prize_name)
        else:
            # 抽奖代码
            now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))
            try:
                info, _ = Info.objects.get_or_create(defaults={
                    'start_time': now,
                    'end_time': now
                })
            except Info.MultipleObjectsReturned:
                info = Info.objects.last()
            if info.is_open is False or now < info.start_time or now > info.end_time:
                return JsonResponse({'code': 2, 'error': '不在活动时间内', 'message': info.errmsg})
            user = serializer.validated_data['user']
            try:
                rule = Rule.objects.get(user=user)
            except Rule.DoesNotExist:
                return JsonResponse({'code': 3, 'error': '账号不满足活动要求'})
            # 判断是否有次数
            if rule.score < 1:
                return JsonResponse({'code': 4, 'error': '账号已没有活动次数'})
            code = rule.get_order()
            if code is None:
                prize_probs = [prize.probability for prize in prizes]
                total = sum(prize_probs)
                acc = list(self.accumulate(prize_probs))
                sernum = bisect.bisect_right(acc, random.uniform(0, total))
                prize = prizes[sernum]
                serializer.save(
                    ip=ip,
                    prizeName=prize.prize_name,
                    prizeId=prize.code,
                    type=0
                )
                rule.score = rule.score - 1
                rule.save()
            else:
                prize = prizes.get(code=code)  # todo except
                serializer.save(
                    ip=ip,
                    prizeName=prize.prize_name,
                    prizeId=code,
                    type=1,
                )
                rule.score = rule.score - 1
                rule.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def accumulate(weights):
        cur = 0
        for w in weights:
            cur = cur + w
            yield cur