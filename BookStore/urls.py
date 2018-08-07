"""BookStore URL Configuration

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
import os
from django.conf.urls import url,include
from django.contrib import admin
from BookStore import settings
from django.views.static import serve
from apps.goods import urls as goodsurl
from apps.user import urls as userurl
from apps.useroptions import urls as favurl
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
import DjangoUeditor.urls
from apps.user.views import GetVerificationCode,UserRegViewSet
from apps.goods.views import BookCategoryView,BookGoodsView
from apps.useroptions.views import UserCollectViewSet
from rest_framework import  routers

router = routers.DefaultRouter()

router.register(r"code",GetVerificationCode,base_name="code")
router.register(r"users",UserRegViewSet,base_name="user")
router.register(r"category",BookCategoryView,base_name="category")
router.register(r"goods",BookGoodsView,base_name="goods")
router.register(r"userfavs",UserCollectViewSet,base_name="userfavs")



urlpatterns = [
    url('^',include(router.urls)),
    url(r'^admin/', admin.site.urls),
    # JWT
    url(r'^login/', obtain_jwt_token),
    url(r'^(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    # TokenAuthentions
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^ueditor/',include(DjangoUeditor.urls)),


]

