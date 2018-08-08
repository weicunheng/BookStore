import re
from datetime import datetime,timedelta
from BookStore.settings import REGEX_STMT
from django.contrib.auth import get_user_model
from apps.user.models import VerifyCode,UserProfile
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.validators import UniqueValidator

UserModel = get_user_model()

class MobileValidation(serializers.Serializer):
    """
    对手机号进行验证
    """
    mobile = serializers.CharField(max_length=11,min_length=11)



    def validated_mobile(self,mobile):
        """
        :return:
        """
        # 1. 检测是否合法
        if not re.match(REGEX_STMT,mobile):
            raise serializers.ValidationError("手机号不合法")
        # 2. 检测数据库中是否存在
        if UserModel.objects.filter(mobile = mobile).count():
            raise serializers.ValidationError("用户已经存在")
        # 3. 检测频率不能小于60s
        one_mintes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago,mobile=mobile):
            raise serializers.ValidationError("距离上次发送未超过60s")

        return mobile


class UserRegValidation(serializers.ModelSerializer):
    # 用户注册 ： 手机号/用户名   验证码     密码
    code = serializers.CharField(max_length=4,min_length=4,write_only=True,help_text="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 }
                                 )


    # 对username校验 : 不能为空，必须填写，唯一
    username = serializers.CharField(label="用户名",help_text="用户名",required=True,allow_blank=False,
                                     validators=[UniqueValidator(queryset = UserModel.objects.all(), message="用户已经存在")],
                                     error_messages={
                                         "required":"该字段不能为空",
                                     })
    # 对password校验  write_only  不参与序列化，这样的话，序列化后，密码就不会被返回，为了安全
    password = serializers.CharField(label="密码",help_text="密码",required=True,allow_blank=False,
                                     style={'input_type': 'password'},write_only=True,
                                     error_messages={
                                         "required": "该字段不能为空",
                                     }
                                     )

    # 使用django的信号量
    # def create(self, validated_data):
    #     user = super(UserRegValidation,self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validated_code(self, code):

        # 校验是否存在 ,按照手机号筛选，倒序取第一个
        code_obj = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by('-add_time')[0]
        if code_obj:
            if code != code_obj.code:
                raise serializers.ValidationError("验证码错误")

            # 校验验证码是否过期  5 分钟
            one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if code_obj.add_time < one_mintes_ago:
                raise serializers.ValidationError("验证码失效")

        else:
            raise serializers.ValidationError("验证码错误")

    # 不加字段名的验证器作用于所有字段之上。
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs


    class Meta:
        model = UserProfile
        fields = ["username","mobile","code","password"]

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("name", "gender", "birthday", "email", "mobile")