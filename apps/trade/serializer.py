from random import Random
import time
from apps.goods.models import Books
from apps.trade.models import ShoppingCart,OrderInfo,OrderGoods
from rest_framework import serializers
from apps.goods.serializers import BookGoodsViewSerializer
from trade.utils.alipayment import AliPay
from BookStore import  settings


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ("id","name","goods_front_image","shop_price")

class ShopCartDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    books = BookGoodsViewSerializer()

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(min_value=1,required=True,
                                    error_messages={
                                        "min_value":"商品数量不能小于1",
                                        "required":"请选择购买的商品"
                                    })
    books = serializers.PrimaryKeyRelatedField(queryset=Books.objects.all(),required=True)

    # 重写create方法
    def create(self, validated_data):
        """
        如果购物车有数据的话，nums就增加
        如果购物车不存在的话，就创建
        :param validated_data:
        :return:
        """
        user = self.context["request"].user
        nums = validated_data["nums"]
        books = validated_data["books"]

        goods = ShoppingCart.objects.filter(user=user,books=books)
        if goods:

            good = goods[0]
            good.nums += 1
            good.save()

        else:
            good = ShoppingCart.objects.create(**validated_data)

        return good

    def update(self, instance, validated_data):
        instance.nums = validated_data["nums"]
        instance.save()
        return instance



class OrderGoodsSerializer(serializers.ModelSerializer):

    goods = BookGoodsViewSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields="__all__"

class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )


    """
    只能读，不能写的字段
    """
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)
    def get_alipay_url(self,obj):
        alipay = AliPay(appid=settings.app_id,
                        app_notify_url=settings.app_notify_url,
                        app_private_key_path=settings.app_private_key_path,
                        alipay_public_key_path=settings.alipay_public_key_path,
                        return_url=settings.return_url,
                        debug=settings.debug)

        # 生成支付的url
        query_params = alipay.direct_pay(subject = obj.order_sn,
                          out_trade_no = obj.order_sn,
                          total_amount = obj.order_mount,
                          return_url=None)

        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

        return pay_url


    def get_random_str(self):
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))

        return order_sn

    # 对字段进行操作
    def validate(self, attrs):

        attrs["order_sn"] = self.get_random_str()
        return attrs


    class Meta:
        model = OrderInfo
        fields = "__all__"