import ipaddress

import ssl
import certifi

from urllib import request
from urllib import parse

import re
import json
import aiohttp

from smsru_api import template


class SmsRu(template.ABCSmsRu):
    def __init__(self, api_id):
        super().__init__(api_id)

    def _request(self, path, data={}):
        data.update(self.data)
        encoded_data = parse.urlencode(data).encode()
        req = request.Request(f'https://sms.ru{path}', data=encoded_data)
        context = ssl.create_default_context(cafile=certifi.where())
        res = request.urlopen(req,  context=context)
        return json.loads(res.read())

    def send(self, *numbers, message,
             from_name=None, ip_address=None,
             timestamp=None, ttl=None, day_time=False,
             translit=False, test=None, debug=False):
        data = self._collect_data(numbers, message, from_name, ip_address, timestamp, ttl, day_time, translit, test, debug)
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


class AsyncSmsRu(template.ABCSmsRu):
    def __init__(self, api_id):
        super().__init__(api_id)

    async def _request(self, path, data={}):
        data.update(self.data)
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with aiohttp.ClientSession("https://sms.ru", connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.post(path, data=data) as res:
                return await res.json()

    async def send(self, *numbers, message,
                   from_name=None, ip_address=None,
                   timestamp=None, ttl=None, day_time=False,
                   translit=False, test=None, debug=False):
        data = self._collect_data(numbers, message, from_name, ip_address, timestamp, ttl, day_time, translit, test, debug)
        return await self._request('/sms/send', data)

    async def callcheck_add(self, phone):
        return await self._request('/callcheck/add', {'phone': phone})

    async def callcheck_status(self, check_id):
        return await self._request('/callcheck/status', {'check_id': check_id})

    async def status(self, sms_id):
        return await self._request('/sms/status', {'sms_id': sms_id})

    async def cost(self, *numbers, message):
        data = self._collect_data(numbers, message)
        return await self._request('/sms/cost', data)

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
        return await self._request('/stoplist/add', {'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number), 'stoplist_text': comment})

    async def del_stop_list(self, number):
        return await self._request('/stoplist/del', {'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number)})

    async def callbacks(self):
        return await self._request('/callback/get')

    async def add_callback(self, url):
        return await self._request('/callback/add', {'url': url})

    async def del_callback(self, url):
        return await self._request('/callback/del', {'url': url})
