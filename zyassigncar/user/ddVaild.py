import json
import datetime
import requests
from user import config
from . import get_token

AppInfo = config.AppInfo()


class Vaild:
    def __init__(self):
        pass

    # 获取ticket值
    def getTicket(self):
        now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        with open("ticket.json", "r+") as f:
            dict = json.load(f)
        ticket = dict["ticket"]
        expires_in = dict["time"]
        t1 = int(now_time)
        t2 = int(expires_in)
        if (t1 - t2) >= 7000:
            access_token = get_token.is_time()
            try:
                if "error" in access_token:
                    return access_token
            except:
                pass
            payload = {
                'access_token': access_token
            }
            res = requests.get('https://oapi.dingtalk.com/get_jsapi_ticket', params=payload,
                               headers={'Connection': 'close'})
            res2 = res.json()
            if 'ticket' not in res2:
                return {
                    "result": False,
                    "error": res2['errmsg']
                }
            dict = {
                "time": now_time,
                "ticket": res2['ticket'],
                "expires_in": res2["expires_in"]
            }
            with open("ticket.json", "w+") as f:
                json.dump(dict, f)
            return res2['ticket']
        return ticket