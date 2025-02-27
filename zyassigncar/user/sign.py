import time
import random
import string
import hashlib


class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': 'zyTest',
            'jsapi_ticket': jsapi_ticket,
            'timeStamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print('result',string)
        self.ret['signature'] = hashlib.sha1(string.encode("utf-8")).hexdigest()
        return self.ret
