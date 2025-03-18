import ipaddress
from urllib import request
from urllib import parse

import re
import json
import aiohttp

from smsru_api import template


class SmsRu(template.ABCSmsRu):
    def __init__(self, api_id):
        super().__init__(api_id)

    def _request(self, path, data=None):
        if data is None:
            data = self.data
        encoded_data = parse.urlencode(data).encode()
        req = request.Request(f'https://sms.ru{path}', data=encoded_data)
        res = request.urlopen(req)
        return json.loads(res.read())

    def send(self, *numbers, message,
             from_name=None, ip_address=None,
             timestamp=None, ttl=None, day_time=False,
             translit=False, test=None, debug=False):
        self._collect_data(numbers, message, from_name, ip_address, timestamp, ttl, day_time, translit, test, debug)
        return self._request('/sms/send', self.data)

    def status(self, sms_id):
        self._data.update({'sms_id': sms_id})
        return self._request('/sms/status', self.data)

    def cost(self, *numbers, message):
        self._collect_data(numbers, message)
        return self._request('/sms/cost', self.data)

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
        self._data.update({'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number), 'stoplist_text': comment})
        return self._request('/stoplist/add', self.data)

    def del_stop_list(self, number):
        self._data.update({'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number)})
        return self._request('/stoplist/del', self.data)

    def callbacks(self):
        return self._request('/callback/get')

    def add_callback(self, url):
        self._data.update({'url': url})
        return self._request('/callback/add', self.data)

    def del_callback(self, url):
        self._data.update({'url': url})
        return self._request('/callback/del', self.data)


class AsyncSmsRu(template.ABCSmsRu):
    def __init__(self, api_id):
        super().__init__(api_id)

    async def _request(self, path, data=None):
        if data is None:
            data = self.data
        async with aiohttp.ClientSession("https://sms.ru") as session:
            async with session.post(path, data=data) as res:
                return await res.json()

    async def send(self, *numbers, message,
                   from_name=None, ip_address=None,
                   timestamp=None, ttl=None, day_time=False,
                   translit=False, test=None, debug=False):
        self._collect_data(numbers, message, from_name, ip_address, timestamp, ttl, day_time, translit, test, debug)
        return await self._request('/sms/send', self.data)

    async def status(self, sms_id):
        self._data.update({'sms_id': sms_id})
        return await self._request('/sms/status', self.data)

    async def cost(self, *numbers, message):
        self._collect_data(numbers, message)
        return await self._request('/sms/cost', self.data)

    async def balance(self):
        return await self._request('/my/balance')

    async def limit(self):
        return await self._request('/my/limit')

    async def free(self):
        return await self._request('/my/free')

    async def senders(self):
        return await self._request('/my/senders')

    async def stop_list(self):
        return await self._request('/stoplist/get')

    async def add_stop_list(self, number, comment=""):
        self._data.update({'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number), 'stoplist_text': comment})
        return await self._request('/stoplist/add', self.data)

    async def del_stop_list(self, number):
        self._data.update({'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number)})
        return await self._request('/stoplist/del', self.data)

    async def callbacks(self):
        return await self._request('/callback/get')

    async def add_callback(self, url):
        self._data.update({'url': url})
        return await self._request('/callback/add', self.data)

    async def del_callback(self, url):
        self._data.update({'url': url})
        return await self._request('/callback/del', self.data)
