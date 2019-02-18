from django.shortcuts import render
from item.serializers import PrizeSerializer
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
    serializer_class = PrizeSerializer

    def get_queryset(self):
        return Prize.objects.all()

