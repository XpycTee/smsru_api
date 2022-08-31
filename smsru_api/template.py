import re
from abc import ABCMeta
from abc import abstractmethod

import time
import ipaddress


class OutOfPhoneNumbers(Exception):
    pass


class OutOfTimestamp(Exception):
    pass


class ABCSmsRu:
    """ SMS.RU API class.

        :param api_id: Ваш API ключ на главной странице личного кабинета. """
    __metaclass__ = ABCMeta

    def __init__(self, api_id: str):
        self._debug_status = False
        self._api_id = api_id
        self._data = {'api_id': self.api_id, 'json': 1, 'partner_id': 358434}

    @property
    def api_id(self) -> str:
        return self._api_id

    @property
    def data(self) -> dict:
        return self._data

    @abstractmethod
    def _request(self, path: str, data: dict) -> dict:
        """ Запрос на сервер.

            :param path: путь для отправки данных.
            :param data: данные для отправки на сервер.
            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def send(self, *numbers: str, message: str, from_name: str, ip_address: str, timestamp: int,
             ttl: int, day_time: bool, translit: bool, test: bool, debug: bool) -> dict:
        """ Отправка сообщения на сервер SMS.RU.

            :param numbers: Номер телефона получателя (либо несколько номеров до
                100 штук за один запрос). Номер телефона для отправки сообщения, желательно без кода страны. Возможно
                использования и других видов, скрипт удалит все не нужное.
            :param message: Текст сообщения в кодировке UTF-8.
            :param from_name: [Опционально] Имя отправителя (должно быть согласовано с администрацией).
            :param ip_address: [Опционально] В этом параметре вы можете передать нам IP адрес вашего пользователя.
            :param timestamp: [Опционально] Время отложенной отправки.
            :param ttl: [Опционально] Срок жизни сообщения в минутах (от 1 до 1440).
            :param day_time: [Опционально] Учитывает часовой пояс получателя. Если указан этот параметр,
                то параметр time игнорируется.
            :param test: [Опционально] Имитирует отправку сообщения для тестирования. True или False
            :param translit: [Опционально] Переводит все русские символы в латинские.
            :param debug: [Опционально] Включает режим отладки. Все сообщения отправляются с параметром test: True
                если он не указан вручную.
            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def call(self, number: str, ip_address: str) -> dict:
        """ Отправить четырехзначный авторизационный код звонком.

            :param number: Номер телефона получателя. Номер телефона для отправки сообщения, желательно без кода страны.
                Возможно использования и других видов, скрипт удалит все не нужное.
            :param ip_address: [Опционально]. В этом параметре вы можете передать нам IP адрес вашего пользователя.
            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def status(self, sms_id: str) -> dict:
        """ Получение статуса СМС по id.

            :param sms_id: id СМС в системе sms.ru.
            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def cost(self, *numbers: str, message: str) -> dict:
        """ Получение стоимости смс.

             :param numbers: Номер телефона получателя (либо несколько номеров до
                100 штук за один запрос). Номер телефона для отправки сообщения, желательно без кода страны. Возможно
                использования и других видов, скрипт удалит все не нужное.
            :param message: Текст сообщения в кодировке UTF-8.
            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def balance(self) -> dict:
        """ Получение баланса аккаунта.

            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def limit(self) -> dict:
        """ Узнать лимит.

            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def free(self) -> dict:
        """ Узнать бесплатный лимит.

            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def senders(self) -> dict:
        """ Получить одобренных отправителей.

            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def stop_list(self) -> dict:
        """ Получить список номеров в стоп листе.

            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def add_stop_list(self, number: str, comment: str) -> dict:
        """ Добавить телефон в стоп лист.

            :param number: Номер для добавления.
            :param comment: Комментарий.
            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def del_stop_list(self, number: str) -> dict:
        """ Удалить телефон из стоп листа.

            :param number: Номер для удаления.
            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def callbacks(self) -> dict:
        """ Получить список callbacks (webhooks).

            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def add_callback(self, url: str) -> dict:
        """ Добавить callback (webhook).

            :param url: Адрес callback.
            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def del_callback(self, url: str) -> dict:
        """ Удалить callback (webhook).

            :param url: Адрес callback.
            :return: JSON ответ от сервера. """
        pass

    def _collect_data(self, numbers: tuple, message: str,
                      from_name: str = None, ip_address: str = None,
                      timestamp: int = None, ttl: int = None, day_time: bool = False,
                      translit: bool = False, test: bool = None, debug: bool = False):
        if ip_address is not None:
            converted_ip = ipaddress.ip_address(ip_address)
            if not (type(converted_ip) is ipaddress.IPv4Address or type(converted_ip) is ipaddress.IPv6Address):
                raise ValueError('Неверно указан ip адрес.')
        if test is None:
            test = debug
        self._debug_status = debug

        if len(numbers) < 100:
            numbers = [re.sub(r'^(\+?7|8)|\D', '', i) for i in numbers]
            self._data.update({'to': ','.join(numbers)})
        else:
            raise OutOfPhoneNumbers('Количество номеров телефонов не может быть больше 100 за один запрос.')

        self._data.update({'text': message})
        if test:
            self._data.update({'test': 1})
        if from_name is not None:
            self._data.update({'from': from_name})
        if timestamp is not None:
            if int(time.time()) - timestamp > 5184000:
                raise OutOfTimestamp('Задержка сообщения не может быть больше 60 дней.')
            self._data.update({'time': int(timestamp)})
        if ttl is not None:
            if ttl > 1440:
                raise OutOfTimestamp('TTL не может быть больше 1440 минут.')
            elif ttl < 1:
                raise OutOfTimestamp('TTL не может быть меньше 1 минуты.')
            self._data.update({'ttl': int(ttl)})
        if day_time:
            self._data.update({'daytime': 1})
        if ip_address is not None:
            self._data.update({'ip': ip_address})
        if translit:
            self._data.update({'translit': 1})
