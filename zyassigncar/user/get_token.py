import requests
from user import config
import json
import datetime
AppInfo = config.AppInfo()
token_dict = {}
def getToken():
    url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (
        AppInfo.AppKey, AppInfo.AppSecret)
    payload = {'AppKey': AppInfo.AppKey, 'AppSecret': AppInfo.AppSecret}
    res = requests.get(url, params=payload)
    result = res.json()
    access_token = result['access_token']
    print("access_token", access_token)
    expires_in = result['expires_in']
    get_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    token_dict['access_token'] = access_token
    token_dict['expires_in'] = expires_in
    token_dict['time'] = get_time
    with open("token.json", "w+") as f:
        json.dump(token_dict, f)
    return token_dict['access_token']


def is_time():
    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        with open('token.json', "r+") as f:
            token_dict = json.load(f)
        access_token = token_dict["access_token"]

        expires_in = token_dict['time']
        t1 = int(now_time)
        t2 = int(expires_in)
        # 判断token是否过期 过期调用getToken重新获取
        if (t1 - t2) >= 7150:
            print(t1 - t2)
            return getToken()
        return access_token
    except Exception as e:
        print("e", e)
        return getToken()
