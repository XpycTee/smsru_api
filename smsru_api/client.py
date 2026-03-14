import re

import httpx

from smsru_api import template


class Client(template.BaseClient):
    """Синхронный клиент для работы с API `sms.ru`."""

    def __init__(self, api_id):
        super().__init__(api_id)
        self._base_url = "https://sms.ru"
        self._client = None

    def __enter__(self):
        if self._client is None:
            self._client = httpx.Client()
        self._managed_mode = True
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def close(self):
        self._managed_mode = False
        if self._client is not None:
            self._client.close()
            self._client = None

    def _get_client(self):
        if not self.managed_mode:
            return None
        if self._client is None:
            raise RuntimeError("Managed client is not available. Re-enter the context manager or create a new client.")
        return self._client

    def _request(self, path, data=None):
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
        return self._request('/stoplist/add',
                             {'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number), 'stoplist_text': comment})

    def del_stop_list(self, number):
        return self._request('/stoplist/del', {'stoplist_phone': re.sub(r'^(\+?7|8)|\D', '', number)})

    def callbacks(self):
        return self._request('/callback/get')

    def add_callback(self, url):
        return self._request('/callback/add', {'url': url})

    def del_callback(self, url):
        return self._request('/callback/del', {'url': url})
