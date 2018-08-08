from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,ListModelMixin,RetrieveModelMixin
from apps.useroptions.models import UserFav
from apps.useroptions.serializers import UserCollectSerializer,UserCollectDetailSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from utils.permissions import IsOwnerOrReadOnly

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