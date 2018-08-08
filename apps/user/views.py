import random
from django.shortcuts import render
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from apps.user.serializer import MobileValidation,UserRegValidation
from apps.user.models import VerifyCode,UserProfile
from apps.utils.YunPianTool import YunPian
from BookStore.settings import YUNPIAN_APIKEY
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler


class GetVerificationCode(CreateModelMixin,GenericViewSet):

    serializer_class = MobileValidation
    queryset = VerifyCode.objects.all()

    def getRandCode(self):
        data = "0123456789"
        l = []
        for i in range(4):
            l.append(random.choice(data))
        return "".join(l)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        moblie = serializer.validated_data["mobile"]

        code = self.getRandCode()
        # 发送验证码再保存

        yunpian = YunPian(YUNPIAN_APIKEY)
        sms_status = yunpian.send_sms(code,moblie)
        if sms_status["code"] != 0:
            # 发送失败
            return Response({
                "mobile": sms_status["msg"]
            },status=status.HTTP_401_UNAUTHORIZED)

        # 短信发送成功，在向数据库中保存验证码
        VerifyCode(code=code,moblie=moblie).save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserRegViewSet(CreateModelMixin,GenericViewSet):
    """
    用户注册
    list:
        xxxxlist
    create:
        创建用户\n
        使用post请求,需要数据：手机号/用户名、验证码、密码\n
        返回：注册成功，返回token；注册失败，返回401\n
    Request Body:
        手机号/用户名、验证码、密码,json格式
    """
    serializer_class = UserRegValidation
    queryset = UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        # 因为password 填写了write_only 所以 ,序列化后的数据 没有passwrod
        """
        print(serializer)
        print(serializer.data)
        """
        """
        用户注册完后，返回一个token
        即可自动登陆，无需注册后，拿着用户名和密码在次登陆
        """

        payload = jwt_payload_handler(user)
        token_data = serializer.data
        token_data["token"] =jwt_encode_handler(payload)
        token_data["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(token_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()