from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.useroptions.models import UserFav

# 第一个参数是接受哪种参数
# 第二个参数是接受哪个model的信号
@receiver(post_save,sender=UserFav)
def create_user(sender, instance=None, created=False, **kwargs):
    """
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        book = instance.books
        book.fav_num += 1
        book.save()

    