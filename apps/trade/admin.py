from django.contrib import admin
from apps.trade import models

admin.site.register(models.ShoppingCart)
admin.site.register(models.OrderInfo)
admin.site.register(models.OrderGoods)

