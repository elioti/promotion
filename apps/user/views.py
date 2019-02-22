from django.shortcuts import render
from rest_framework import viewsets
from user.serializers import AdminSerializer
from user.models import SiteAdmin
from django_filters import rest_framework
from utils.views import GoodsPagination
from rest_framework import filters
# Create your views here.


class AdminViewSet(viewsets.ModelViewSet):
    serializer_class = AdminSerializer
    queryset = SiteAdmin.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ('username', 'id')
    ordering_fields = ('username', 'id')
