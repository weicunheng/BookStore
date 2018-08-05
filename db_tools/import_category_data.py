import os
import sys

#当前文件路径
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BookStore.settings")

import django
django.setup()

from apps.goods.models import BooksCategory
from db_tools.data.category_data import row_data
#
# for category1 in row_data:
#     instance1 = BooksCategory()
#     instance1.name = category1["name"]
#     instance1.code = category1["code"]
#     instance1.category_type = 1
#     instance1.save()
#
#     for category2 in category1["sub_categorys"]:
#         instance2 = BooksCategory()
#         instance2.name = category2["name"]
#         instance2.code = category2["code"]
#         instance2.category_type = 2
#         instance2.parent_category = instance1
#         instance2.save()
#
#         for category3 in category2["sub_categorys"]:
#             instance3 = BooksCategory()
#             instance3.name = category3["name"]
#             instance3.code = category3["code"]
#             instance3.category_type = 3
#             instance3.parent_category = instance2
#             instance3.save()

for lev1_cat in row_data:
    lev1_intance = BooksCategory()
    lev1_intance.code = lev1_cat["code"]
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.category_type = 1
    lev1_intance.save()

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_intance = BooksCategory()
        lev2_intance.code = lev2_cat["code"]
        lev2_intance.name = lev2_cat["name"]
        lev2_intance.category_type = 2
        lev2_intance.parent_category = lev1_intance
        lev2_intance.save()

        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_intance = BooksCategory()
            lev3_intance.code = lev3_cat["code"]
            lev3_intance.name = lev3_cat["name"]
            lev3_intance.category_type = 3
            lev3_intance.parent_category = lev2_intance
            lev3_intance.save()