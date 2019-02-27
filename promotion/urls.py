"""promotion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from main.views import AdminViewSet, PrizeViewSet, RuleViewSet, RecViewSet, InfoViewSet
from rest_framework_jwt.views import obtain_jwt_token
router = DefaultRouter()
router.register(r'prizes', PrizeViewSet, base_name='prizes')
router.register(r'records', RecViewSet, base_name='records')
router.register(r'users', AdminViewSet, base_name='users')
router.register(r'rules', RuleViewSet, base_name='rules')
router.register(r'infos', InfoViewSet, base_name='info')
urlpatterns = [
    url(r'login', obtain_jwt_token),
    url(r'', include(router.urls)),

]
