from rest_framework import serializers
from apps.useroptions.models import UserFav
from rest_framework.validators import UniqueTogetherValidator
from apps.goods.models import Books


class BooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = ("id","name","shop_price")


class UserCollectDetailSerializer(serializers.ModelSerializer):
    books = BooksSerializer()

    class Meta:
        model = UserFav
        fields = ("books",)


class UserCollectSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserFav
        # 对UniqueTogetherValidator进行约束
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'books'),
                message="已经收藏"
            )
        ]
        fields=("user","books","id")
