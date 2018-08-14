from django.apps import AppConfig


class UseroptionsConfig(AppConfig):
    name = 'apps.useroptions'
    verbose_name = "用户操作配置"

    def ready(self):
        import apps.goods.signals