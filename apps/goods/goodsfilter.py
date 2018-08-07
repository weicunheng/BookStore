import django_filters
from apps.goods.models import Books
from django.db.models import Q


class BooksListFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    # field_name 是作用哪个字段
    price__min = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gt')
    price__max = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lt')

    # 模糊查询，用于全文搜索  大小写忽略、标题、详细内容
    # 如果不指定lookup_expr，全匹配
    # name = django_filters.CharFilter(name="name",lookup_expr='icontains')

    class Meta:
        model = Books
        fields = ['price__min','price__max',"name","is_hot"]