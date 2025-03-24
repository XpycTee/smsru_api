import re
from abc import ABCMeta
from abc import abstractmethod

import time
import ipaddress


class OutOfPhoneNumbers(Exception):
    pass


class OutOfTimestamp(Exception):
    pass


class BaseClient:
    """ SMS.RU API class.

        :param api_id: Ваш API ключ на главной странице личного кабинета. """
    __metaclass__ = ABCMeta

    def __init__(self, api_id: str):
        self._debug_status = False
        self._api_id = api_id
        self._def_data = {
            'api_id': self.api_id,  # API ключ
            'json': 1,  # Возвращать ответ в формате JSON
            'partner_id': 358434  # ID партнера, прошу если вы будете использовать мой код, не меняйте его, это то что мотивирует меня поддерживапть данное api, спасибо ツ
        }

    @property
    def api_id(self) -> str:
        return self._api_id

    @property
    def defaults(self) -> dict:
        return self._def_data

    @abstractmethod
    def _request(self, path: str, data: dict) -> dict:
        """ Запрос на сервер.

            :param path: путь для отправки данных.
            :param data: данные для отправки на сервер.
            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def send(self, *numbers: str, message: str, multi: dict, from_name: str, ip_address: str, timestamp: int,
             ttl: int, day_time: bool, translit: bool, test: bool, debug: bool, partner_id: int) -> dict:
        """ Отправка сообщения на сервер SMS.RU.

            :param numbers: Номер телефона получателя (либо несколько номеров до
                100 штук за один запрос). Номер телефона для отправки сообщения, желательно без кода страны. Возможно
                использования и других видов, скрипт удалит все не нужное.
            :param message: Текст сообщения в кодировке UTF-8.
            :param multi: Отправка сообщения на несколько номеров с разными текстами, если указан этот параметр, то параметры numbers и message игнорируются.
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
            :param partner_id: [Опционально] ID партнера (для агентов).
            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def callcheck_add(self, phone: str) -> dict:
        """ Добавление номера в callcheck.

            :param phone: Номер телефона пользователя, который необходимо авторизовать (с которого мы будем ожидать звонок).
            :return: JSON ответ от сервера. """
        pass

    @abstractmethod
    def callcheck_status(self, check_id: str) -> dict:
        """ Проверка статуса звонка.

            :param check_id: Идентификатор авторизации, полученный от sms.ru при добавлении номера.
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

    def _collect_data(self, numbers: tuple, message: str = None, multi=None,
                      from_name: str = None, ip_address: str = None,
                      timestamp: int = None, ttl: int = None, day_time: bool = False,
                      translit: bool = False, test: bool = None, debug: bool = False,
                      partner_id: int = None) -> dict:
        if multi is None:
            multi = {}
        if len(numbers) > 100 or len(multi) > 100:
            raise OutOfPhoneNumbers('Количество номеров телефонов не может быть больше 100 за один запрос.')

        data = {}

        if ip_address is not None:
            converted_ip = ipaddress.ip_address(ip_address)
            if not (type(converted_ip) is ipaddress.IPv4Address or type(converted_ip) is ipaddress.IPv6Address):
                raise ValueError('Неверно указан ip адрес.')
        if test is None:
            test = debug
        self._debug_status = debug

        if multi:
            multi_data = {}
            for key, value in multi.items():
                multi_data[f'to[{key}]'] = value
            data.update(multi_data)
        else:
            if not message:
                raise ValueError('Не указан текст сообщения')
            if not numbers:
                raise ValueError('Не указан номер(а) телефона')
            numbers = [re.sub(r'^(\+?7|8)|\D', '', i) for i in numbers]
            data.update({'to': ','.join(numbers)})
            data.update({'text': message})

        if test:
            data.update({'test': 1})
        if from_name is not None:
            data.update({'from': from_name})
        if timestamp is not None:
            if int(time.time()) - timestamp > 5184000:
                raise OutOfTimestamp('Задержка сообщения не может быть больше 60 дней.')
            data.update({'time': int(timestamp)})
        if ttl is not None:
            if ttl > 1440:
                raise OutOfTimestamp('TTL не может быть больше 1440 минут.')
            elif ttl < 1:
                raise OutOfTimestamp('TTL не может быть меньше 1 минуты.')
            data.update({'ttl': int(ttl)})
        if day_time:
            data.update({'daytime': 1})
        if ip_address is not None:
            data.update({'ip': ip_address})
        if translit:
            data.update({'translit': 1})
        if partner_id is not None:
            data.update({'partner_id': partner_id})

        return data  # Возвращаем новый объект данных

