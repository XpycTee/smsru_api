from typing import Optional

import httpx

from smsru_api import template


class AsyncClient(template.AsyncBaseClient):
    """Асинхронный клиент для работы с API `sms.ru`.

    Все публичные методы класса являются coroutine и должны вызываться через
    `await`.
    """

    def __init__(self, api_id: str):
        super().__init__(api_id)
        self._base_url = "https://sms.ru"
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "AsyncClient":
        if self._client is None:
            self._client = httpx.AsyncClient()
        self._managed_mode = True
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        self._managed_mode = False
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _get_client(self) -> Optional[httpx.AsyncClient]:
        if not self.managed_mode:
            return None
        if self._client is None:
            raise RuntimeError("Managed async client is not available. Re-enter the context manager or create a new client.")
        return self._client

    async def _request(self, path: str, data: Optional[template.RequestData] = None) -> template.JsonDict:
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

    async def send(
        self,
        *numbers: str,
        message: Optional[str] = None,
        multi: Optional[template.MultiMessageMap] = None,
        from_name: Optional[str] = None,
        ip_address: Optional[str] = None,
        timestamp: Optional[int] = None,
        ttl: Optional[int] = None,
        day_time: bool = False,
        translit: bool = False,
        test: Optional[bool] = None,
        debug: bool = False,
        partner_id: Optional[int] = None,
    ) -> template.JsonDict:
        data = self._collect_data(
            numbers,
            message=message,
            multi=multi,
            from_name=from_name,
            ip_address=ip_address,
            timestamp=timestamp,
            ttl=ttl,
            day_time=day_time,
            translit=translit,
            test=test,
            debug=debug,
            partner_id=partner_id,
        )
        return await self._request('/sms/send', data)

    async def callcheck_add(self, phone: str) -> template.JsonDict:
        return await self._request('/callcheck/add', {'phone': phone})

    async def callcheck_status(self, check_id: str) -> template.JsonDict:
        return await self._request('/callcheck/status', {'check_id': check_id})

    async def status(self, sms_id: str) -> template.JsonDict:
        return await self._request('/sms/status', {'sms_id': sms_id})

    async def cost(self, *numbers: str, message: str) -> template.JsonDict:
        data = self._collect_data(numbers, message=message)
        return await self._request('/sms/cost', data)

    async def balance(self) -> template.JsonDict:
        return await self._request('/my/balance')

    async def limit(self) -> template.JsonDict:
        return await self._request('/my/limit')

    async def free(self) -> template.JsonDict:
        return await self._request('/my/free')

    async def senders(self) -> template.JsonDict:
        return await self._request('/my/senders')

    async def stop_list(self) -> template.JsonDict:
        return await self._request('/stoplist/get')

    async def add_stop_list(self, number: str, comment: str = "") -> template.JsonDict:
        data: template.RequestData = {
            'stoplist_phone': self._normalize_and_validate_phone(number),
            'stoplist_text': comment,
        }
        return await self._request('/stoplist/add', data)

    async def del_stop_list(self, number: str) -> template.JsonDict:
        data: template.RequestData = {'stoplist_phone': self._normalize_and_validate_phone(number)}
        return await self._request('/stoplist/del', data)

    async def callbacks(self) -> template.JsonDict:
        return await self._request('/callback/get')

    async def add_callback(self, url: str) -> template.JsonDict:
        return await self._request('/callback/add', {'url': url})

    async def del_callback(self, url: str) -> template.JsonDict:
        return await self._request('/callback/del', {'url': url})
