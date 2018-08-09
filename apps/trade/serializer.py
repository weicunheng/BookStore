from apps.trade.models import ShoppingCart
from rest_framework import serializers

class ShopCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = ShoppingCart
        fields = "__all__"