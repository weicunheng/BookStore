from django.contrib import admin
from apps.goods import models


admin.site.register(models.BooksCategory)
admin.site.register(models.Publishers)
admin.site.register(models.Authors)
admin.site.register(models.Books)
admin.site.register(models.IndexAd)
admin.site.register(models.BooksImage)
admin.site.register(models.Banner)
admin.site.register(models.HotSearchWords)