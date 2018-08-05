from django.conf.urls import url,include
from apps.user.views import GetVerificationCode,UserRegViewSet
from rest_framework import  routers

router = routers.DefaultRouter()
router.register(r"code",GetVerificationCode)
router.register(r"users",UserRegViewSet)


urlpatterns=[
    url(r'^',include(router.urls)),
]