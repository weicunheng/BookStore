from random import Random
import time
from apps.goods.models import Books
from apps.trade.models import ShoppingCart,OrderInfo
from rest_framework import serializers
from apps.goods.serializers import BookGoodsViewSerializer


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



class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ("id","order_sn","add_time","order_mount","pay_status","post_script")

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # # 订单金额
    # order_mount = serializers.IntegerField(allow_null=False)
    # # 收货人手机号
    # singer_mobile = serializers.CharField(max_length=11,allow_null=False,allow_blank=False)
    #
    # # 收货人
    # signer_name = serializers.CharField(max_length=40,allow_null=True,allow_blank=True,default="")
    # # 用户收货地址
    # address = serializers.CharField(max_length=100,allow_null=False,allow_blank=False)
    #
    # # 用户留言
    # post_script = serializers.CharField(max_length=200,allow_null=True,allow_blank=True)

    """
    只能读，不能写的字段
    
    """
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)


    def get_random_str(self):
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))

        return order_sn

    # 对字段进行操作
    def validate(self, attrs):

        attrs["order_sn"] = self.get_random_str()
        print(attrs["order_sn"])
        return attrs


    class Meta:
        model = OrderInfo
        # fields = ("user","order_mount","singer_mobile","signer_name","address","post_script")
        fields = "__all__"