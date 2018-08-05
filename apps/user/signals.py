from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


# 接受User  model传来的信号
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # 如果是新建操作
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()

        # 如果使用的是TokenAuthention认证的时候使用；这里我们使用的是JWT，所以就不使用了
        # Token.objects.create(user=instance)