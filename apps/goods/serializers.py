from apps.goods import models
from rest_framework import serializers

class BookCategorySerilizer3(serializers.ModelSerializer):
    class Meta:
        model = models.BooksCategory
        fields = "__all__"
class BookCategorySerilizer2(serializers.ModelSerializer):
    sub_cat = BookCategorySerilizer3(many=True)
    class Meta:
        model = models.BooksCategory
        fields = "__all__"

class BookCategorySerilizer(serializers.ModelSerializer):
    #利用反向查询字段
    sub_cat = BookCategorySerilizer2(many=True)
    class Meta:
        model = models.BooksCategory
        fields = "__all__"


# 商品 主图  序列化
class GoodImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BooksImage
        fields=("image",)


class BookGoodsViewSerializer(serializers.ModelSerializer):
    category = BookCategorySerilizer()
    images = GoodImagesSerializer(many=True)

    class Meta:
        model = models.Books
        fields = "__all__"