from .serializers import AdminSerializer, PrizeSerializer, RuleSerializer, RecSerializer, MemberRecSerializer, InfoSerializer
from rest_framework import viewsets
from .models import *
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from utils.permission import IsSuperUser
from django_filters import rest_framework
from django.http.response import JsonResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, authentication
from django.contrib.auth.hashers import make_password
import bisect
import random
import datetime
from django.utils import timezone
import pytz
from django.db.models import Min
# Create your views here.


class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperUser,)
    serializer_class = AdminSerializer
    queryset = SiteAdmin.objects.all().order_by('id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.OrderingFilter,)
    ordering_fields = ('id',)

    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data['password']), is_staff=True)


class PrizeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all().order_by('id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ('prize_name', 'id', 'grade')
    ordering_fields = ('prize_name', 'id')

    def list(self, request, *args, **kwargs):
        if request.query_params.get('type', None):
            prizes = Prize.objects.all()
            categorys = Prize.objects.values('grade').distinct()
            context = []
            for category in categorys:
                context.append({
                    'name': category['grade'] or '其他',
                    'prizes': self.get_serializer(prizes.filter(grade=category['grade']), many=True).data
                })
            return JsonResponse(context, safe=False)
        else:
            return super(PrizeViewSet, self).list(self, request, *args, **kwargs)


class RuleViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )
    serializer_class = RuleSerializer
    queryset = Rule.objects.all().order_by('id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ('user', 'id')
    ordering_fields = ('id',)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.kwargs[self.lookup_field] == 'all':
            Rule.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return super(RuleViewSet, self).destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        if isinstance(serializer.validated_data, list):
            validated_data = [
                dict(list(attrs.items()))
                for attrs in serializer.validated_data
            ]
            Rule.objects.bulk_create([Rule(**item) for item in validated_data])
        else:
            serializer.save()


class InfoViewSet(viewsets.ModelViewSet):
    serializer_class = InfoSerializer
    queryset = Info.objects.all().order_by('id')


class RecFilter(rest_framework.FilterSet):
    min_rec = rest_framework.NumberFilter(field_name="id", lookup_expr='gt')

    class Meta:
        model = Rec
        fields = ['user', 'min_rec']


class RecViewSet(viewsets.ModelViewSet):
    serializer_class = RecSerializer
    queryset = Rec.objects.all().order_by('id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_class = RecFilter
    ordering_fields = ('id',)

    def get_permissions(self):
        params = self.request.query_params
        if self.action in ['create', 'list']:
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return RecSerializer
        else:
            return MemberRecSerializer

    def partial_update(self, request, *args, **kwargs):
        if self.kwargs[self.lookup_field] == 'send':
            Rec.objects.filter(isSend=0).update(isSend=1, sendTime=timezone.now())
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            instance = self.get_object()
            flag = request.data.get('isSend', None)
            if flag is None:
                return super(RecViewSet, self).partial_update(request, *args, **kwargs)
            else:
                if flag == 2 and instance.isSend == 0:
                    serializer = self.get_serializer(instance, {'isSend': 2, 'censor': request.user.username}, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data)  # 锁定成功
                if flag == 1 and request.user.username == instance.censor:
                    serializer = self.get_serializer(instance, {'isSend': 1, 'sendTime': timezone.now()}, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data)  # 派送成功
                else:
                    print(flag, request.user, instance.censor)
                    return Response({'code': 1, 'error': '该记录已被锁定', 'data': self.get_serializer(instance).data})  # 操作失败

    def list(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super(RecViewSet, self).list(request, *args, **kwargs)
        else:
            user = request.query_params.get('user', None)
            if user is not None:
                recs = Rec.objects.filter(user=user).order_by('-datetime')
                page = self.paginate_queryset(recs)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(recs, many=True)
                return Response(serializer.data)
            else:
                recs = Rec.objects.all().order_by('-datetime')[0:30]
                data = [{
                    'user': rec.user[:2] + '***',
                    'prizeName': rec.prizeName,
                } for rec in recs]
            return Response(data)

    def destroy(self, request, *args, **kwargs):
        if self.kwargs[self.lookup_field] == 'all':
            Rec.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return super(RecViewSet, self).destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'HTTP_X_FORWARDED_FOR' in self.request.META.values():
            ip = self.request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = self.request.META['REMOTE_ADDR']
        if self.request.user.is_staff:
            serializer.save(ip=ip, type=2)
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
            except Rule.MultipleObjectsReturned:
                rule = Rule.objects.last()
            action = request.data.get('action', None)
            if action and action == 'login':
                return JsonResponse({'code': 4, 'user': rule.user, 'score': rule.score})
            # 判断是否有次数
            if rule.score < 1:
                return JsonResponse({'code': 5, 'error': '账号已没有活动次数'})
            code = rule.get_order()
            if code is None:
                prizes = Prize.objects.filter(grade=rule.type)
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
                prize = Prize.objects.get(code=code, grade=rule.type)  # todo except
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


