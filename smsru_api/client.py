import ssl
import certifi

from urllib import request
from urllib import parse

import re
import json

from smsru_api import template


class Client(template.BaseClient):
    def __init__(self, api_id):
        super().__init__(api_id)

    def _request(self, path, data=None):
        if data is None:
            data = {}
        request_data = self.defaults.copy()
        request_data.update(data)
        encoded_request = parse.urlencode(request_data).encode()
        req = request.Request(f'https://sms.ru{path}', data=encoded_request)
        context = ssl.create_default_context(cafile=certifi.where())
        res = request.urlopen(req,  context=context)
        return json.loads(res.read())

    def send(self, *numbers, **kwargs):
        data = self._collect_data(numbers, **kwargs)
        return self._request('/sms/send', data)

    def callcheck_add(self, phone):
        return self._request('/callcheck/add', {'phone': phone})
    
    def callcheck_status(self, check_id):
        return self._request('/callcheck/status', {'check_id': check_id})

    def status(self, sms_id):
        return self._request('/sms/status', {'sms_id': sms_id})

    def cost(self, *numbers, message):
        data = self._collect_data(numbers, message)
        return self._request('/sms/cost', data)

    def balance(self):
        return self._request('/my/balance')

    def limit(self):
        return self._request('/my/limit')

    def free(self):
        return self._request('/my/free')

    def senders(self):
        return self._request('/my/senders')

    def stop_list(self):
        return self._request('/stoplist/get')

    def add_stop_list(self, number, comment=""):
        return self._request('/stoplist/add', {'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number), 'stoplist_text': comment})

    def del_stop_list(self, number):
        return self._request('/stoplist/del', {'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number)})

    def callbacks(self):
        return self._request('/callback/get')

    def add_callback(self, url):
        return self._request('/callback/add', {'url': url})

    def del_callback(self, url):
        return self._request('/callback/del', {'url': url})
