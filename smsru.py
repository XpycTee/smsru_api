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
        self.__debug_status = False
        self.api_id = api_id

    def debugging(self, message):
        """ Debug опвещение в консоль
            :param message: Сообщение отправляемое в консоль """
        if self.__debug_status:
            print('Debug:', message)

    def send(self, numbers: list, message: str, from_name: str, ip_address: str, timestamp: int,
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

    def send(self, numbers, message, from_name=None, ip_address=None, timestamp=None,
             ttl=None, day_time=False, translit=False, test=None, debug=False):
        converted_ip = ipaddress.ip_address(ip_address)
        if not (type(converted_ip) is ipaddress.IPv4Address or type(converted_ip) is ipaddress.IPv6Address):
            raise ValueError('Неверно указан ip адрес')
        if test is None:
            test = debug
        self.__debug_status = debug
        url_message = parse.quote(message)
        to_data = {"to": None}
        for number in numbers:
            phone_replace = re.compile(r'^(\+?7|8)|\D')
            number = phone_replace.sub('', number)
            if len(numbers) < 100:
                if to_data['to'] is None:
                    to_data['to'] = f'7{number}'
                else:
                    to_data['to'] += f',7{number}'
            else:
                raise OutOfPhoneNumbers('Количетсво номеров телефонов не может быть больше 100')
        data = parse.urlencode(to_data)
        to_numbers = ''
        if len(numbers) < 10:
            to_numbers = '&' + data
        url = f"http://sms.ru/sms/send?api_id={self.api_id}{to_numbers}&text={url_message}&partner_id=358434&json=1"
        if test:
            url = "%s&test=1" % url
        if from_name is not None:
            url = "%s&from=%s" % (url, from_name)
        if timestamp is not None:
            if int(time.time()) - timestamp > 5184000:
                raise OutOfTimestamp('Задержка сообщения не может быть больше 60 дней')
            url = "%s&time=%d" % (url, int(timestamp))
        if ttl is not None:
            if ttl > 1440:
                raise OutOfTimestamp('TTL не может быть больше 1440 минут')
            elif ttl < 1:
                raise OutOfTimestamp('TTL не может быть меньше 1 минуты')
            url = "%s&ttl=%d" % (url, int(ttl))
        if day_time:
            url = "%s&daytime=1" % url
        if ip_address is not None:
            url = "%s&ip=%s" % (url, ip_address)
        if translit:
            url = '%s&translit=1' % url
        req = request.Request(url, data=data.encode())
        res = request.urlopen(req)
        self.debugging("GET: %s %s\nReply:\n%s" % (res.geturl(), res.msg, res.info()))
        response = json.loads(res.read())
        self.debugging(response)
        return response

