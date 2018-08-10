from apps.goods.models import Books
from apps.trade.models import ShoppingCart,OrderInfo
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ("id","name","goods_front_image","shop_price")

class ShopCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    books = BookSerializer()

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCartCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    books = serializers.PrimaryKeyRelatedField(required=True,queryset=Books.objects.all())

    # def validated_books(self,books):
    #     book_obj = Books.objects.filter(books=books).count()
    #     if not book_obj:
    #         raise serializers.ValidationError("书籍不存在，添加失败")
    #     return book_obj

    class Meta:
        model = ShoppingCart
        fields =("books","user","nums")


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ("id","order_sn","add_time","order_mount","post_script")

class OrderSerializer(serializers.ModelSerializer):
    """
    { 'signer_name': '张三', 'singer_mobile': '13611229745', 'order_mount': 160}
    user = mode
    order_sn =
    trade_no =
    pay_status
    post_script
    order_mount
    pay_time =
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # 订单金额
    order_mount = serializers.IntegerField(allow_null=False)
    # 收货人手机号
    singer_mobile = serializers.CharField(max_length=11,allow_null=False,allow_blank=False)

    # 收货人
    signer_name = serializers.CharField(max_length=40,allow_null=True,allow_blank=True,default="")
    # 用户收货地址
    address = serializers.CharField(max_length=100,allow_null=False,allow_blank=False)

    # 用户留言
    post_script = serializers.CharField(max_length=200,allow_null=True,allow_blank=True)

    class Meta:
        model = OrderInfo
        # fields
        fields = ("user","order_mount","singer_mobile","signer_name","address","post_script")