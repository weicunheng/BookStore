#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback
from BookStore import settings
from Crypto.PublicKey import RSA
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


if __name__ == '__main__':
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    alipay_client_config = AlipayClientConfig(sandbox_debug=False)
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2016091700533057'
    alipay_client_config.app_private_key = "MIIEpQIBAAKCAQEA2FudQ6FY7Zox7GfutOK5Gp349j+0ZrY/SBoO13t+IZUms50Fyq+C4emXQ/xmwDmxX6/sBQeUgS45UOmXNPpHnSPwUwwLkOtBwxlWnz/Yijy3q/juSjg7OQe6jaGaZB/Rz7KtqxkJkuFXWs7C8DwpGsuAn72tYMwRlBofEItOQXjYUg+GMEvYsZMyx/PXRMDa8pZKFSOx4VTwrKrvOdCH9Krg+BbKAcXmj0+NHPI+vAhWn4MyZx5c/hqqIqnmY/gaVoCQkpJjFZ+t1fe21YAdoNbEX+x5lJe11qVjVxfxcGGDLMwvhAt6bzhSMy1kqKoYa3BiQnPOSy8c/ZhobX1XOQIDAQABAoIBAHN5+mcVX+R5TzoRguuSsx9Mv4uXFs9XaFEwb0l9hSWheOWW4nd6082GIpFLzv+8Czq6J6vLjuyf4kGYW3cQOlbZzrRUknvHxPK/vGcE6atmmtWz6GM+vgVDZcOgREo6XX6QrHbMxzpZAYnbH1qfkYTWpxEbaMVoRd2ZT4lCAQOZ48nXpTTh52xytNSbHYjugSIs+7UHk/Ls+dIa+uVScK7936BQQlWP0BPvif7feFL2EK0ycqbo10ZjqNKROuvugFo1uYeWj6eR8l57z/63aeGV6xRBgGQE7/h6+Aol7Kg1AxOdkMOQJh01yQ/h0r9OqsYxp9EYuFvdQd/S8/em9l0CgYEA9hHgsxcMq7V27NctcVc9m03tZz4emUgS4eyIlMQ8dN3su9mFaQkvid4rjwDivZyNS/ukWSsITMIO5si7nJbX8G0XhulbR7F/Lbb9musDC/xKUDX1LWswicnEEo0P8nD6AP/IMDjWSL8Mubb630upGOwC3WDVwdj0A70jtf+KjxcCgYEA4RbJCT0DKQt2zZ6DciRuh2mY3co5irjw7pO39jSyJZ+3DHYfPyF7qKtCWdqA9uJ4I4HO99ibbEmFJix5YEw2HD/5nN+3fyxJ0nmUtIzosWjUZ/hA2HE7wfwoS64NXLKeg3s2AqMxjT/fjXc09BYrs7EiE/w3grgVRxLLvzI2vi8CgYEA3Ajyf9JtnyGeXXywgvg6+6P8VOTEYdaEJAfpvfWYBfzokrWYyWrQWp0TIEXvexQBeV9k/+MuAc1Jm+8FbKmqILC8aARFfl9m1Q8byaq6x73rCbymJ94AwkVskhYXm3iQ5dHTReOdIeHM1EieHow+gi2RBjpwCm4hDTLVOwpt8TMCgYEAm8z8vHNJ47g2tJ7a10AWbY6PLD3U1Ius4UbIWBgjk11ZA7wjZrxTbu2UEMPo7nrVs6YfT3jUJAFDs6enIBvAfI9fxNEpn1JViuVzJAJA8sPf+lNg9zBxr5VNgwzn3NkaVWIMgYjaPK4QnEf+FFHgUBH0x6aV+dpXiAmflCk6sSsCgYEAm5h+JtiuIoWTEJ+zUCFSPYMSE0FiTjQKJfyUOuUR22l/MSqk8UFUE+xDmk5sBCHNXp+pvo8z5tsFglY50qrBigWAjjyQL00QOdQA9M0EYz8cZ5B9W5bZO42FYASKlTFvJtZs0/P4EFgOPeDlj1UgUpgbIBGGl1zoGgLtk85nH5U="
    alipay_client_config.alipay_public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAltj6/yXI0htgB18KIogveTv7r9MM091hufQ+KPpGPT0Ta8flWw+abZdgCska7fVWKaZyfv11sstYpzhhZxgtForNBgCVooQr8LT0/6wwy80kNNbVWkWCzu22QQYGG373Al/OIHnffDgPD0GYgpDtGWtC8QSqJpVnAXHG3QiL8puNnSutT8H7UUXMj6DEgE1AuMu6LlcAhBsew9jhCTEsJ/iGZ6I1kWtGrawFYS71m+fRuMNmrEufZ94M8ePwqMLxoUg6wgN1Dk8iSqCIjeOdcvlYwrxgrcrM4rekCSaxnoFwD7VhR3qtOKvV8/n4Ydzweh2/bs6rUbb29VU/vXVWdQIDAQAB"

    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)

    """
    页面接口示例：alipay.trade.page.pay
    """
    # 对照接口文档，构造请求对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = "pay201805020000226"
    model.total_amount = 50
    model.subject = "测试"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    
    settle_detail_info = SettleDetailInfo()
    settle_detail_info.amount = 50
    settle_detail_info.trans_in_type = "userId"
    settle_detail_info.trans_in = "2088302300165604"
    settle_detail_infos = list()
    settle_detail_infos.append(settle_detail_info)
    settle_info = SettleInfo()
    settle_info.settle_detail_infos = settle_detail_infos
    model.settle_info = settle_info
    sub_merchant = SubMerchant()
    sub_merchant.merchant_id = "2088102176051162"
    model.sub_merchant = sub_merchant
    request = AlipayTradePagePayRequest(biz_model=model)
    request.return_url = "http://47.94.172.250:8804/page2/"
    request.notify_url = "http://47.94.172.250:8804/page2/"
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    response = client.page_execute(request, http_method="GET")
    print("alipay.trade.page.pay response:" + response)
    import time
    time.sleep(1000)

    """
    https://openapi.alipaydev.com/gateway.do?
    timestamp=2018-08-13+15%3A10%3A43&
    app_id=2016091700533057&
    method=alipay.trade.page.pay&
    charset=utf-8&
    format=json&
    version=1.0&
    sign_type=RSA2&sign=kFQhVQ0opjGiSZ34K1CRC9xQSROYVF8gQmfizXJ4MtlnP3pAWYfVjqZpRwxL6%2BFRSZ4OX8ldF345cbLOAV8Sz04ajTqcru7qnU6qj0OBhYMjBgqRCJyam7iyCK31BsgaOgyxSDTGFq9TvD00BEsP%2BIYo2KJLzM%2Fleeo6vCQAmiHnMIonXIwWVd8lTDN0fJYPipz9BsuaxZQ6lngA3jzZ14sMmptOdZwflhin%2F4sWYHeyTnc275jz7BDFqL3zkvvmvWtIgG7zL9X4VVbxY6IJqswvvQxx%2BupUkYwkI6xGFE%2FWif%2BwKdEaiNoGYwsRl4xR012B2RSv7vC8CMHtQlcN5A%3D%3D&
    biz_content=%7B%22body%22%3A%22%E6%94%AF%E4%BB%98%E5%AE%9D%E6%B5%8B%E8%AF%95%22%2C%22out_trade_no%22%3A%2220150320010101001%22%2C%22product_code%22%3A%22FAST_INSTANT_TRADE_PAY%22%2C%22settle_info%22%3A%7B%22settle_detail_infos%22%3A%5B%7B%22amount%22%3A50%7D%5D%7D%2C%22sub_merchant%22%3A%7B%22merchant_id%22%3A%222088102176051162%22%7D%2C%22subject%22%3A%22%E6%B5%8B%E8%AF%95%22%2C%22total_amount%22%3A50%7D
    """