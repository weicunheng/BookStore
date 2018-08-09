from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,ListModelMixin,RetrieveModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet

from utils.permissions import IsOwnerOrReadOnly
from apps.useroptions.models import UserFav,UserAddress
from apps.useroptions.serializers import UserCollectSerializer,UserCollectDetailSerializer,AddressSerializer
# 对于收藏： 添加收藏和删除收藏
class UserCollectViewSet(ListModelMixin,CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,GenericViewSet):
    # queryset = UserFav.objects.all()
    serializer_class = UserCollectSerializer
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    # 拒绝任何未认证用户  和  只能进行实例所属的操作
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)

    # /userfavs/5/获取某一个收藏的详情
    lookup_field = "books_id"

    def get_serializer_class(self):
        if self.action == "list":
            return UserCollectDetailSerializer
        elif self.action == "create":
            return UserCollectSerializer
        return UserCollectSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)



# 收获地址
class AddressViewSet(ModelViewSet):
    """
        收货地址管理
        list:
            获取收货地址
        create:
            添加收货地址
        update:
            更新收货地址
        delete:
            删除收货地址
    """
    queryset = UserAddress.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

