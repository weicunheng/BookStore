from django.conf.urls import url,include
from apps.goods.views import BookCategoryView,BookGoodsView
from rest_framework import  routers

router = routers.DefaultRouter()
router.register(r"category",BookCategoryView)
router.register(r"goods",BookGoodsView)

urlpatterns=[
    url(r'^',include(router.urls)),
    # url(r'category/(?P<category_id>\d+)/',BookCategoryView.as_view()),
]