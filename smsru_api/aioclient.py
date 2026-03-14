import re

import httpx

from smsru_api import template


class AsyncClient(template.BaseClient):
    """Асинхронный клиент для работы с API `sms.ru`.

    Все публичные методы класса являются coroutine и должны вызываться через
    `await`.
    """

    def __init__(self, api_id):
        super().__init__(api_id)
        self._base_url = "https://sms.ru"
        self._client = None

    async def __aenter__(self):
        if self._client is None:
            self._client = httpx.AsyncClient()
        self._managed_mode = True
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.aclose()

    async def aclose(self):
        self._managed_mode = False
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _get_client(self):
        if not self.managed_mode:
            return None
        if self._client is None:
            raise RuntimeError("Managed async client is not available. Re-enter the context manager or create a new client.")
        return self._client

    async def _request(self, path, data=None):
        if data is None:
            data = {}
        request_data = self.defaults.copy()
        request_data.update(data)
        url = self._base_url + path
        client = self._get_client()
        if client is not None:
            response = await client.post(url, data=request_data)
            response.raise_for_status()
            return response.json()

        async with httpx.AsyncClient() as temporary_client:
            response = await temporary_client.post(url, data=request_data)
            response.raise_for_status()
            return response.json()

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
