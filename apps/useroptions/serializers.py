from rest_framework import serializers
from apps.useroptions.models import UserFav
from rest_framework.validators import UniqueTogetherValidator
from apps.goods.serializers import BookGoodsViewSerializer



class UserCollectSerializer(serializers.ModelSerializer):
    # books = BookGoodsViewSerializer
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
