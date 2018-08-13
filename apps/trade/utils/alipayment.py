from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from base64 import decodebytes, encodebytes
import json


class AliPay(object):
    """
    支付宝支付接口(PC端支付接口)
    """

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        """
        :param appid: APPID
        :param app_notify_url:
        :param app_private_key_path: app私钥文件路径
        :param alipay_public_key_path: 阿里公钥路径
        :param return_url: 支付宝支付成功回调url
        :param debug: 是否是沙箱环境
        """
        self.appid = appid
        self.app_notify_url = app_notify_url
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        self.return_url = return_url
        # self.debug = True

        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())
        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:

            # 主要是验证支付宝给我们返回消息的时候，用来判断身份
            self.alipay_public_key = RSA.importKey(fp.read())

        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"


    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        biz_content = {

            "subject": subject,  #订单标题
            "out_trade_no": out_trade_no,  # 商品订单号
            "total_amount": total_amount,  #  金额
            "product_code": "FAST_INSTANT_TRADE_PAY",  #销售产品码
            # "qr_pay_mode":4
        }

        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)

        # 构建sign参数
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        """
        构建请求公共参数
        :param method:接口名称
        :param biz_content: 业务请求参数集合
        :param return_url:回调地址
        :return:
        """
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        """
        商户请求参数的签名串,
        1).APPID，2).应用私钥，3).支付宝公钥，配置在代码中，对请求内容进行签名，并对支付宝返回的内容进行验签
         1. 筛选并排序
         2. 拼接
         3. 调用签名函数
         4. 把生成的签名赋值给sign参数，拼接到请求参数中
        :param data:公共参数集合
        :return:签名串
        """
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        # ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        """
        开始计算签名
        :param unsigned_string:
        :return:
        """
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        """
        支付成功后，支付宝会自动调用return_url
        此时我们需要对支付宝发来的请求进行验证
        防止被拦截修改数据

        把里面的sign pop出去，然后对剩下的部分进行签名，
        将签名之后的字符串与原来的进行比对就知道是否合法了。
        :param data:
        :param signature:
        :return:
        """
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)

        return self._verify(message, signature)
