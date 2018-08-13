from datetime import datetime
from BookStore import settings
from apps.trade.models import ShoppingCart,OrderInfo,OrderGoods
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from apps.trade.serializer import ShopCartSerializer,ShopCartDetailSerializer,OrderSerializer,OrderDetailSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from trade.utils.alipayment import AliPay
from rest_framework.response import Response


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
class OrderViewSet(ListModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
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
        if self.action == "retrieve":
            return OrderDetailSerializer
        elif self.action == "create":
            return OrderSerializer
        return OrderSerializer




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


# 支付宝支付
class AlipayView(APIView):
    def get(self,request):
        """
        支付成功，支付宝会同步通知get请求服务器。扫码支付成功
        :param request:
        :return:
        """
        data = {}
        for key,value in request.GET.items():
            data[key] = value

        sign = data.pop("sign", None)
        # 2. 创建AliPay对象
        alipay = AliPay(appid=settings.app_id,
                        app_notify_url=settings.app_notify_url,
                        app_private_key_path=settings.app_private_key_path,
                        alipay_public_key_path=settings.alipay_public_key_path,
                        return_url=settings.return_url,
                        debug=settings.debug)

        # 3. 进行验签，确保这是支付宝给我们的
        isverify = alipay.verify(data, signature=sign)

        if isverify:
            # 获取订单状态
            order_sn = data.get("out_trade_no",None)
            trade_no = data.get("trade_no",None)
            pay_status = data.get('trade_status', None)

            order_objs = OrderInfo.objects.filter(order_sn = order_sn)
            for order_obj in order_objs:
                # 订单商品项
                order_goods = order_obj.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                # 更新订单状态，填充支付宝给的交易凭证号。
                order_objs.trade_no = trade_no
                order_objs.pay_status = pay_status

                order_obj.pay_time = datetime.now()
                order_objs.save()


            # 跳转
            return Response()

    def post(self,request):
        """
        支付成功，支付宝会根据notify_url异步通知，通过post请求将参数传给商户。通过未支付订单
        :param request:
        :return:
        """
        # 1. 从请求中取出数据,将sign剔除
        data = {}
        for key,value in  request.POST.items():
            data[key] = value

        sign = data.pop("sign",None)

        # 2. 创建AliPay对象
        alipay = AliPay(appid=settings.app_id,
                        app_notify_url=settings.app_notify_url,
                        app_private_key_path=settings.app_private_key_path,
                        alipay_public_key_path=settings.alipay_public_key_path,
                        return_url=settings.return_url,
                        debug=settings.debug)

        # 3. 进行验签，确保这是支付宝给我们的
        isverify = alipay.verify(data,signature=sign)


        # 如果校验成功，修改数据库
        if isverify:
            # 获取订单状态
            order_sn = data.get("out_trade_no",None)
            trade_no = data.get("trade_no",None)
            pay_status = data.get('trade_status', None)

            order_objs = OrderInfo.objects.filter(order_sn = order_sn)
            for order_obj in order_objs:
                # 订单商品项
                order_goods = order_obj.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                # 更新订单状态，填充支付宝给的交易凭证号。
                order_objs.trade_no = trade_no
                order_objs.pay_status = pay_status

                order_obj.pay_time = datetime.now()
                order_objs.save()


            # 给支付宝
            return Response("success")

