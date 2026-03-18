from typing import Optional

import httpx

from smsru_api import template


class Client(template.BaseClient):
    """Синхронный клиент для работы с API `sms.ru`."""

    def __init__(self, api_id: str):
        super().__init__(api_id)
        self._base_url = "https://sms.ru"
        self._client: Optional[httpx.Client] = None

    def __enter__(self) -> "Client":
        if self._client is None:
            self._client = httpx.Client()
        self._managed_mode = True
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def close(self) -> None:
        self._managed_mode = False
        if self._client is not None:
            self._client.close()
            self._client = None

    def _get_client(self) -> Optional[httpx.Client]:
        if not self.managed_mode:
            return None
        if self._client is None:
            raise RuntimeError("Managed client is not available. Re-enter the context manager or create a new client.")
        return self._client

    def _request(self, path: str, data: Optional[template.RequestData] = None) -> template.JsonDict:
        if data is None:
            data = {}
        request_data = self.defaults.copy()
        request_data.update(data)
        url = self._base_url + path
        client = self._get_client()
        if client is not None:
            response = client.post(url, data=request_data)
            response.raise_for_status()
            return response.json()

        with httpx.Client() as temporary_client:
            response = temporary_client.post(url, data=request_data)
            response.raise_for_status()
            return response.json()

    def send(
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
        return self._request('/sms/send', data)

    def callcheck_add(self, phone: str) -> template.JsonDict:
        return self._request('/callcheck/add', {'phone': phone})

    def callcheck_status(self, check_id: str) -> template.JsonDict:
        return self._request('/callcheck/status', {'check_id': check_id})

    def status(self, sms_id: str) -> template.JsonDict:
        return self._request('/sms/status', {'sms_id': sms_id})

    def cost(self, *numbers: str, message: str) -> template.JsonDict:
        data = self._collect_data(numbers, message=message)
        return self._request('/sms/cost', data)

    def balance(self) -> template.JsonDict:
        return self._request('/my/balance')

    def limit(self) -> template.JsonDict:
        return self._request('/my/limit')

    def free(self) -> template.JsonDict:
        return self._request('/my/free')

    def senders(self) -> template.JsonDict:
        return self._request('/my/senders')

    def stop_list(self) -> template.JsonDict:
        return self._request('/stoplist/get')

    def add_stop_list(self, number: str, comment: str = "") -> template.JsonDict:
        return self._request(
            '/stoplist/add',
            {'stoplist_phone': self._normalize_and_validate_phone(number), 'stoplist_text': comment},
        )

    def del_stop_list(self, number: str) -> template.JsonDict:
        return self._request('/stoplist/del', {'stoplist_phone': self._normalize_and_validate_phone(number)})

    def callbacks(self) -> template.JsonDict:
        return self._request('/callback/get')

    def add_callback(self, url: str) -> template.JsonDict:
        return self._request('/callback/add', {'url': url})

    def del_callback(self, url: str) -> template.JsonDict:
        return self._request('/callback/del', {'url': url})
