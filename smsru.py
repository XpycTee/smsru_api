from urllib import request
from urllib import parse
from abc import ABCMeta
from abc import abstractmethod

import time
import re
import json
import ipaddress
import aiohttp


class OutOfPhoneNumbers(Exception):
    pass


class OutOfTimestamp(Exception):
    pass


class ABCSmsRu:
    """ SMS.RU API class
            :param api_id: Ваш API ключ на главной странице личного кабинета """
    __metaclass__ = ABCMeta

    def __init__(self, api_id):
        self._debug_status = False
        self._api_id = api_id
        self._data = {'api_id': self.api_id, 'json': 1, 'partner_id': 358434}

    @property
    def api_id(self):
        return self._api_id

    @property
    def data(self):
        return self._data

    @abstractmethod
    def _request(self, path, data):
        """ Запрос на сревер
            :param path: путь для отправки данных
            :param data: данные для отправки на сервер
            :return response: Ответ от сервера """
        pass

    @abstractmethod
    def send(self, numbers: list[str], message: str, from_name: str, ip_address: str, timestamp: int,
             ttl: int, day_time: bool, translit: bool, test: bool, debug: bool):
        """ Отправка сообщения на сервер SMS.RU
                :param numbers: Номер телефона получателя (либо несколько номеров до
                100 штук за один запрос). Номер телефона для отправки сообщения, желатьельно без кода страны. Возможно
                исполльзования и других видов, скрипт удалит все не нужное.
                :param message: Текст сообщения в кодировке UTF-8 .
                :param from_name: [Опционально] Имя отправителя (должно быть согласовано с администрацией).
                :param ip_address: [Опционально] В этом параметре вы можете передать нам  IP адрес вашего пользователя.
                :param timestamp: [Опционально] Время отложенной отправки.
                :param ttl: [Опционально] Срок жизни сообщения в минутах (от 1 до 1440).
                :param day_time: [Опционально] Учитывает часовой пояс получателя. Если указан этот параметр,
                то параметр time игнорируется.
                :param test: [Опционально] Имитирует отправку сообщения для тестирования. True или False
                :param translit: [Опционально] Переводит все русские символы в латинские.
                :param debug: [Опционально] Включает режим отладки. Все собщения отправляются с парпметром test: True
                если он не указан в ручную
                :return response: Ответ от сервера """
        pass

    def _collect_data(self, numbers, message,
                      from_name, ip_address,
                      timestamp, ttl, day_time,
                      translit, test, debug):
        if ip_address is not None:
            converted_ip = ipaddress.ip_address(ip_address)
            if not (type(converted_ip) is ipaddress.IPv4Address or type(converted_ip) is ipaddress.IPv6Address):
                raise ValueError('Неверно указан ip адрес')
        if test is None:
            test = debug
        self._debug_status = debug

        if len(numbers) < 100:
            numbers = [re.sub(r'^(\+?7|8)|\D', '', i) for i in numbers]
            self._data.update({'to': ','.join(numbers)})
        else:
            raise OutOfPhoneNumbers('Количетсво номеров телефонов не может быть больше 100 за одн запрос')

        self._data.update({'text': message})
        if test:
            self._data.update({'test': 1})
        if from_name is not None:
            self._data.update({'from': from_name})
        if timestamp is not None:
            if int(time.time()) - timestamp > 5184000:
                raise OutOfTimestamp('Задержка сообщения не может быть больше 60 дней')
            self._data.update({'time': int(timestamp)})
        if ttl is not None:
            if ttl > 1440:
                raise OutOfTimestamp('TTL не может быть больше 1440 минут')
            elif ttl < 1:
                raise OutOfTimestamp('TTL не может быть меньше 1 минуты')
            self._data.update({'ttl': int(ttl)})
        if day_time:
            self._data.update({'daytime': 1})
        if ip_address is not None:
            self._data.update({'ip': ip_address})
        if translit:
            self._data.update({'translit': 1})


class SmsRu(ABCSmsRu):
    def __init__(self, api_id):
        super().__init__(api_id)

    def _request(self, path, data=None):
        if data is None:
            data = self.data
        encoded_data = parse.urlencode(data).encode()
        req = request.Request(f'https://sms.ru{path}', data=encoded_data)
        res = request.urlopen(req)
        return json.loads(res.read())

    def send(self, numbers, message,
             from_name=None, ip_address=None,
             timestamp=None, ttl=None, day_time=False,
             translit=False, test=None, debug=False):
        self._collect_data(numbers, message, from_name, ip_address, timestamp, ttl, day_time, translit, test, debug)
        return self._request('/sms/send', self.data)

    def status(self, sms_id):
        self._data.update({'sms_id': sms_id})
        return self._request('/sms/status', self.data)

    def cost(self, numbers, message):
        self._collect_data(numbers, message, None, None, None, None, False, False, None, False)
        return self._request('/sms/cost', self.data)

    def balance(self):
        return self._request('/my/balance')

    def limit(self):
        return self._request('/my/limit')

    def senders(self):
        return self._request('/my/senders')


class AsyncSmsRu(ABCSmsRu):
    def __init__(self, api_id):
        super().__init__(api_id)

    async def _request(self, path, data=None):
        if data is None:
            data = self.data
        async with aiohttp.ClientSession("https://sms.ru") as session:
            async with session.post(path, data=data) as res:
                return await res.json()

    async def send(self, numbers, message,
                   from_name=None, ip_address=None,
                   timestamp=None, ttl=None, day_time=False,
                   translit=False, test=None, debug=False):
        self._collect_data(numbers, message, from_name, ip_address, timestamp, ttl, day_time, translit, test, debug)
        return await self._request('/sms/send', self.data)

    async def status(self, sms_id):
        self._data.update({'sms_id': sms_id})
        return await self._request('/sms/status', self.data)

    async def cost(self, numbers, message):
        self._collect_data(numbers, message, None, None, None, None, False, False, None, False)
        return await self._request('/sms/cost', self.data)

    async def balance(self):
        return await self._request('/my/balance')

    async def limit(self):
        return await self._request('/my/limit')

    async def senders(self):
        return await self._request('/my/senders')
