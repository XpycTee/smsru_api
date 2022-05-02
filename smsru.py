from urllib import request
from urllib import parse

import time
import re
import json
import ipaddress


class OutOfPhoneNumbers(Exception):
    pass


class OutOfTimestamp(Exception):
    pass


class ISmsRu:
    """ SMS.RU API class
            :param api_id: Ваш API ключ на главной странице личного кабинета """

    def __init__(self, api_id):
        self._debug_status = False
        self._api_id = api_id
        self.data = {'api_id': self.api_id, 'json': 1, 'partner_id': 358434}

    @property
    def api_id(self):
        return self._api_id

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


class SmsRu(ISmsRu):
    def __init__(self, api_id):
        super().__init__(api_id)

    def send(self, numbers, message,
             from_name=None, ip_address=None,
             timestamp=None, ttl=None, day_time=False,
             translit=False, test=None, debug=False):
        if ip_address is not None:
            converted_ip = ipaddress.ip_address(ip_address)
            if not (type(converted_ip) is ipaddress.IPv4Address or type(converted_ip) is ipaddress.IPv6Address):
                raise ValueError('Неверно указан ip адрес')
        if test is None:
            test = debug
        self._debug_status = debug

        url = f"https://sms.ru/sms/send"

        if len(numbers) < 100:
            numbers = [re.sub(r'^(\+?7|8)|\D', '', i) for i in numbers]
            self.data.update({'to': ','.join(numbers)})
        else:
            raise OutOfPhoneNumbers('Количетсво номеров телефонов не может быть больше 100 за одн запрос')

        self.data.update({'text': message})
        if test:
            self.data.update({'test': 1})
        if from_name is not None:
            self.data.update({'from': from_name})
        if timestamp is not None:
            if int(time.time()) - timestamp > 5184000:
                raise OutOfTimestamp('Задержка сообщения не может быть больше 60 дней')
            self.data.update({'time': int(timestamp)})
        if ttl is not None:
            if ttl > 1440:
                raise OutOfTimestamp('TTL не может быть больше 1440 минут')
            elif ttl < 1:
                raise OutOfTimestamp('TTL не может быть меньше 1 минуты')
            self.data.update({'ttl': int(ttl)})
        if day_time:
            self.data.update({'daytime': 1})
        if ip_address is not None:
            self.data.update({'ip': ip_address})
        if translit:
            self.data.update({'translit': 1})
        data = parse.urlencode(self.data).encode()
        req = request.Request(url, data=data)
        res = request.urlopen(req)
        response = json.loads(res.read())
        return response

