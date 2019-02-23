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
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from item.views import PrizeViewSet
from member.views import RecViewSet
from user.views import AdminViewSet
from rest_framework_jwt.views import obtain_jwt_token
from utils.views import ObtainSessionWebToken
router = DefaultRouter()
router.register(r'prizes', PrizeViewSet, base_name='prizes')
router.register(r'records', RecViewSet, base_name='records')
router.register(r'users', AdminViewSet, base_name='users')
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include(router.urls)),
    url(r'^login', ObtainSessionWebToken.as_view()),
    # url(r'login', obtain_jwt_token),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
