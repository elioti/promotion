from django.shortcuts import render
from item.serializers import PrizeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from item.models import Prize
from django_filters import rest_framework as filters
from rest_framework import filters
from django_filters import rest_framework
# Create your views here.


class PrizeViewSet(viewsets.ModelViewSet):
    """
    list:
    create:
    update:
    delete:
    """
    # permission_classes = (IsAuthenticated, )
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ('code', 'id')
    ordering_fields = ('code', 'id')

