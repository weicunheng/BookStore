from apps.trade.models import ShoppingCart
from rest_framework.viewsets import ModelViewSet
from apps.trade.serializer import ShopCartSerializer



# 购物车
class ShopCartView(ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShopCartSerializer

