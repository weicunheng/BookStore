from django.contrib import admin
from apps.useroptions import models

admin.site.register(models.UserFav)
admin.site.register(models.UserLeavingMessage)
admin.site.register(models.UserAddress)