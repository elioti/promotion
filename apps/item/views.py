from django.shortcuts import render
from item.serializers import PrizeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from item.models import Prize
# Create your views here.


class PrizeViewSet(viewsets.ModelViewSet):
    """
    list:
    create:
    update:
    delete:
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()

