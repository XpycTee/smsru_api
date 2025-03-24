import ssl
import certifi

import re
import aiohttp

from smsru_api import template


class AsyncClient(template.BaseClient):
    def __init__(self, api_id):
        super().__init__(api_id)

    async def _request(self, path, data=None):
        if data is None:
            data = {}
        request_data = self.defaults.copy()
        request_data.update(data)
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with aiohttp.ClientSession("https://sms.ru", connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.post(path, data=request_data) as res:
                return await res.json()

    async def send(self, *numbers, **kwargs):
        data = self._collect_data(numbers, **kwargs)
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
        data = {'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number), 'stoplist_text': comment}
        return await self._request('/stoplist/add', data)

    async def del_stop_list(self, number):
        data = {'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number)}
        return await self._request('/stoplist/del', data)

    async def callbacks(self):
        return await self._request('/callback/get')

    async def add_callback(self, url):
        return await self._request('/callback/add', {'url': url})

    async def del_callback(self, url):
        return await self._request('/callback/del', {'url': url})
