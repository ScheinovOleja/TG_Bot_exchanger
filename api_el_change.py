import urllib
from pprint import pprint

import requests as req
from datetime import datetime
import hashlib
import hmac


class Test:

    def __init__(self):
        self.api_password = b'vm2zJwKbJzukAm8iTaMS'
        self.unix_time = datetime.now().timestamp()

    def export(self):
        text_from_hmac = {
            'date_start': '2019-10-21 13:00:00',
            'date_end': '2019-12-23 00:00:00',
            'page_num': 1,
            'records_limit': 2,
            'interface_lang': 'ru',
            'api_name': 'pythonbot',
            'unix_time': self.unix_time
        }
        text = urllib.parse.urlencode(text_from_hmac).encode('utf8')
        data_hmac = hmac.new(self.api_password, text, hashlib.sha512).hexdigest()
        header = {
            'HMAC': data_hmac
        }
        result = req.post(url="https://el-change.com/user_api/get_balances",
                          headers=header,
                          data=text_from_hmac)
        data = result.json()
        return data


if __name__ == '__main__':
    bot = Test()
    pprint(bot.export())
    # print(json)
