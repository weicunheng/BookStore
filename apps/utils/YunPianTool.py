'''
name:weiheng
用于发送短信验证码
'''
import requests

class YunPian(object):
    def __init__(self,apikey):
        self.api_key = apikey
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"


    def send_sms(self,code,mobile):
        params = {
            'apikey': self.api_key,
            'text': f"【魏恒】短信验证码为:{code},如果不是本人，请忽略。",
            'mobile':mobile
        }
        response = requests.post(
            url=self.single_send_url,
            data=params,
            headers={
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"
            }
        )


