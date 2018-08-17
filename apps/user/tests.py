from django.test import TestCase
import requests



def get_authorize():
    client_id = "3539749669"
    redirect_uri = "http://127.0.0.1:8000/"
    url = "https://api.weibo.com/oauth2/authorize?client_id={}&redirect_uri={}".format(client_id,redirect_uri)

    print(url)

    # ret = requests.get(
    #     url = url
    # )
    # print(ret)


def get_auth_token():
    code = "57abbb5446a7e9856173e4257e540bb4"
    client_id = "3539749669"
    client_secret="fd0a20e70eb877bdf766fd4341e999ae"
    redirect_uri = "http://127.0.0.1:8000/"

    # https://api.weibo.com/oauth2/access_token?client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&grant_type=authorization_code&redirect_uri=YOUR_REGISTERED_REDIRECT_URI&code=CODE
    url = "https://api.weibo.com/oauth2/access_token?client_id={}&client_secret={}&grant_type=authorization_code&redirect_uri={}&code={}".format(
        client_id,
        client_secret,
        redirect_uri,
        code
    )

    print(url)
    ret = requests.post(
        url=url
    )
    print(ret.text)

def get_user_info():
    access_token = "2.00X_HcqFba7YrDb00216d1eceXZtcD"
    uid = "56598631a7f3ffb7ccf680697f544afe"
    screen_name="Toreadwh"
    url = "https://api.weibo.com/2/users/show.json?access_token=%s&screen_name=%s"%(access_token,screen_name)
    print(url)
    ret = requests.get(
        url=url
    )
    print(ret.text)


if __name__ == "__main__":
    # get_authorize()
    # get_auth_token()
    get_user_info()