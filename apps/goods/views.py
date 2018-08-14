from rest_framework import pagination
from apps.goods.models import BooksCategory,Books,Banner
from rest_framework import mixins
from rest_framework  import viewsets,filters
from apps.goods.serializers import BookCategorySerilizer,BookGoodsViewSerializer,BannerViewSerializer
from apps.goods.goodsfilter import BooksListFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle


# 图书分类
class BookCategoryView(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = BooksCategory.objects.filter(category_type=1)
    serializer_class = BookCategorySerilizer


# 图书分页
class BookPagination(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


# 图书
class BookGoodsView(CacheResponseMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):


    # UnorderedObjectListWarning 解决
    queryset = Books.objects.all().order_by("id")
    serializer_class = BookGoodsViewSerializer
    pagination_class = BookPagination
    throttle_classes = (UserRateThrottle,AnonRateThrottle)

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    #自定义过滤规则
    filter_class = BooksListFilter
    #对哪些字段进行搜索
    search_fields = ('name', 'goods_brief','goods_desc')
    #指定哪些字段进行排序过滤
    ordering_fields = ('sold_num', 'shop_price')


    def retrieve(self, request, *args, **kwargs):
        """
        修改商品点击量
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# Banner
class BannerView(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    获取Banner列表
    """
    serializer_class = BannerViewSerializer
    queryset = Banner.objects.all().order_by("index")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

