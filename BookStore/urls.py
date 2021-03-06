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
from django.conf.urls import url, include
from django.contrib import admin
from BookStore import settings
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
import DjangoUeditor.urls
from apps.user.views import GetVerificationCode, UserRegViewSet
from apps.goods.views import BookCategoryView, BookGoodsView, BannerView
from apps.useroptions.views import UserCollectViewSet, AddressViewSet
from apps.trade.views import ShopCartView, OrderViewSet
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from apps.trade.views import AlipayView

schema_view = get_schema_view(title='图书商城API文档')
router = routers.DefaultRouter()

router.register(r"code", GetVerificationCode, base_name="code")
router.register(r"users", UserRegViewSet, base_name="user")
router.register(r"category", BookCategoryView, base_name="category")
router.register(r"goods", BookGoodsView, base_name="goods")
router.register(r"userfavs", UserCollectViewSet, base_name="userfavs")
router.register(r"address", AddressViewSet, base_name="address")
router.register(r"shopcarts", ShopCartView, base_name="shopcarts")
router.register(r"orders", OrderViewSet, base_name="orders")
router.register(r"banners", BannerView, base_name="banners")

urlpatterns = [
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^', include(router.urls)),
    url(r'^schema/$', schema_view),
    url(r'^docs/', include_docs_urls(title="图书商城")),
    url(r'^admin/', admin.site.urls),
    # JWT
    url(r'^login/$', obtain_jwt_token),
    url(r'^(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    # TokenAuthentions
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^ueditor/', include(DjangoUeditor.urls)),
    url(r'^alipay/return/', AlipayView.as_view(), name="alipay"),

]
