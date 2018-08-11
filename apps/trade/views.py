import time
from random import Random

from apps.trade.models import ShoppingCart,OrderInfo,OrderGoods
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from apps.trade.serializer import ShopCartSerializer,ShopCartDetailSerializer,OrderSerializer,OrderDetailSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import  status


# 购物车
class ShopCartView(ModelViewSet):

    serializer_class = ShopCartSerializer
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)

    lookup_field = "books_id"

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)
        #get_serializer_class
    def get_serializer_class(self):
        if self.action == "create":
            print(self.request.data)
            return ShopCartSerializer
        elif self.action == "list":
            return ShopCartDetailSerializer
        return ShopCartSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 订单是不允许被修改的
class OrderViewSet(ListModelMixin,CreateModelMixin,DestroyModelMixin,GenericViewSet):
    """
        订单管理
        list:
            获取个人订单
        delete:
            删除订单
        create：
            新增订单
        """

    serializer_class = OrderSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


    def get_serializer_class(self):
        if self.action == "list":
            return OrderDetailSerializer
        elif self.action == "create":
            return OrderSerializer
        return OrderSerializer


    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     print(serializer.validated_data["user"])
    #
    #     # 订单号
    #     random_ins = Random()
    #     order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
    #                                                    userid=request.user.id,
    #                                                    ranstr=random_ins.randint(10, 99))
    #     # pay_status = "paying"
    #     # OrderInfo(user=request.user,
    #     #           order_mount=serializer.validated_data["order_mount"],
    #     #           singer_mobile = serializer.validated_data["singer_mobile"],
    #     #           signer_name = serializer.validated_data["signer_name"],
    #     #           address = serializer.validated_data["address"],
    #     #           post_script = serializer.validated_data["post_script"],
    #     #           order_sn=order_sn,
    #     #           pay_status=pay_status).save()
    #     # order = OrderInfo.objects.filter(user = request.user).order_by("-add_time").first()
    #     # self.clear_cart(order)
    #     headers = self.get_success_headers(serializer.data)
    #
    #     ret = serializer.data
    #
    #     # 先完善功能，下次修改
    #     ret["alipay_url"] = "https://www.baidu.com"
    #
    #     return Response(ret, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        order = serializer.save()
        self.clear_cart(order)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)


    def clear_cart(self,order):
        order_goods = OrderGoods()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods.goods = shop_cart.books
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            # 清空购物车
            shop_cart.delete()