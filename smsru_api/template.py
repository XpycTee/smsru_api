import re
from abc import ABC
from abc import abstractmethod

import time
import ipaddress


class OutOfPhoneNumbers(Exception):
    """Ошибка при превышении лимита получателей в одном запросе.

    Исключение выбрасывается, если в `send()` или `cost()` передано больше
    100 номеров через позиционные аргументы или словарь `multi`.
    """


class OutOfTimestamp(Exception):
    """Ошибка при некорректных временных параметрах запроса.

    Используется для проверки отложенной отправки `timestamp` и срока жизни
    сообщения `ttl`.
    """


class BaseClient(ABC):
    """Базовый клиент для работы с HTTP API `sms.ru`.

    Класс инкапсулирует общие параметры авторизации и логику подготовки данных
    для запросов. Публичные методы реализуются в синхронном и асинхронном
    клиентах поверх этого базового интерфейса.

    :param api_id: API-ключ из личного кабинета `sms.ru`.
    """
    def __init__(self, api_id: str):
        self._debug_status = False
        self._api_id = api_id
        self._managed_mode = False
        self._def_data = {
            'api_id': self.api_id,  # API ключ
            'json': 1,  # Возвращать ответ в формате JSON
            'partner_id': 358434  # ID партнера, прошу если вы будете использовать мой код, не меняйте его, это то что мотивирует меня поддерживать данный api, спасибо ツ
        }

    @property
    def api_id(self) -> str:
        """Вернуть API-ключ, с которым создан клиент."""
        return self._api_id

    @property
    def defaults(self) -> dict:
        """Вернуть словарь базовых параметров для каждого запроса.

        В словарь входят `api_id`, признак JSON-ответа и партнерский
        идентификатор по умолчанию.
        """
        return self._def_data

    @property
    def managed_mode(self) -> bool:
        """Показывает, используется ли клиент в режиме контекстного менеджера."""
        return self._managed_mode

    @abstractmethod
    def _request(self, path: str, data: dict) -> dict:
        """Отправить подготовленный запрос на сервер `sms.ru`.

        :param path: Путь метода API, например `/sms/send`.
        :param data: Данные формы, которые нужно отправить в запросе.
        :return: JSON-ответ сервера, преобразованный в словарь Python.
        """
        pass

    @abstractmethod
    def send(self, *numbers: str, message: str, multi: dict, from_name: str, ip_address: str, timestamp: int,
             ttl: int, day_time: bool, translit: bool, test: bool, debug: bool, partner_id: int) -> dict:
        """Отправить SMS-сообщение через API `sms.ru`.

        Метод поддерживает два режима:

        - передача общего текста через `numbers` и `message`;
        - передача словаря `multi`, где ключом является номер телефона, а
          значением текст сообщения. В этом случае `numbers` и `message`
          игнорируются.

        :param numbers: Один или несколько номеров телефона. Перед отправкой
            номера нормализуются: из строки удаляются пробелы, скобки,
            дефисы и ведущий код `+7` или `8`.
        :param message: Общий текст сообщения в кодировке UTF-8.
        :param multi: Словарь вида `{номер: текст}` для отправки разных
            сообщений разным получателям.
        :param from_name: Имя отправителя, согласованное с администрацией
            `sms.ru`.
        :param ip_address: IP-адрес конечного пользователя. Проверяется
            встроенным модулем `ipaddress`.
        :param timestamp: Unix timestamp для отложенной отправки. Значение не
            должно быть больше чем на 60 дней от текущего времени.
        :param ttl: Срок жизни сообщения в минутах, допустимый диапазон от 1
            до 1440.
        :param day_time: Учитывать локальное дневное время получателя.
        :param translit: Транслитерировать кириллический текст.
        :param test: Включить тестовый режим API без фактической отправки.
        :param debug: Включить локальный режим отладки. Если `test` явно не
            задан, значение `debug=True` автоматически включает тестовый режим.
        :param partner_id: Партнерский идентификатор, которым можно
            переопределить значение по умолчанию.
        :return: JSON-ответ сервера, преобразованный в словарь Python.
        :raises OutOfPhoneNumbers: Если передано больше 100 получателей.
        :raises OutOfTimestamp: Если `timestamp` или `ttl` выходят за
            допустимые пределы.
        :raises ValueError: Если отсутствует текст, номер телефона или указан
            некорректный IP-адрес.
        """
        pass

    @abstractmethod
    def callcheck_add(self, phone: str) -> dict:
        """Добавить номер в сценарий авторизации по звонку.

        :param phone: Номер телефона пользователя, звонок с которого нужно
            ожидать для подтверждения.
        :return: JSON-ответ сервера со статусом операции и `check_id`.
        """
        pass

    @abstractmethod
    def callcheck_status(self, check_id: str) -> dict:
        """Проверить статус авторизации по звонку.

        :param check_id: Идентификатор проверки, полученный из `callcheck_add`.
        :return: JSON-ответ сервера с текущим статусом проверки.
        """
        pass

    @abstractmethod
    def status(self, sms_id: str) -> dict:
        """Получить статус ранее отправленного SMS.

        :param sms_id: Идентификатор сообщения в системе `sms.ru`.
        :return: JSON-ответ сервера с кодом и текстом статуса.
        """
        pass

    @abstractmethod
    def cost(self, *numbers: str, message: str) -> dict:
        """Рассчитать стоимость SMS без отправки.

        :param numbers: Один или несколько номеров телефона. Номера проходят
            ту же нормализацию, что и в `send()`.
        :param message: Текст сообщения для оценки стоимости.
        :return: JSON-ответ сервера со стоимостью и деталями расчета.
        :raises OutOfPhoneNumbers: Если передано больше 100 получателей.
        :raises ValueError: Если не передан текст или номер телефона.
        """
        pass

    @abstractmethod
    def balance(self) -> dict:
        """Получить текущий баланс аккаунта `sms.ru`.

        :return: JSON-ответ сервера с балансом аккаунта.
        """
        pass

    @abstractmethod
    def limit(self) -> dict:
        """Получить информацию о доступных лимитах.

        :return: JSON-ответ сервера с лимитами аккаунта.
        """
        pass

    @abstractmethod
    def free(self) -> dict:
        """Получить информацию о бесплатном лимите сообщений.

        :return: JSON-ответ сервера по бесплатным лимитам.
        """
        pass

    @abstractmethod
    def senders(self) -> dict:
        """Получить список одобренных имен отправителя.

        :return: JSON-ответ сервера со списком отправителей.
        """
        pass

    @abstractmethod
    def stop_list(self) -> dict:
        """Получить текущий стоп-лист номеров.

        :return: JSON-ответ сервера со списком номеров в стоп-листе.
        """
        pass

    @abstractmethod
    def add_stop_list(self, number: str, comment: str) -> dict:
        """Добавить номер телефона в стоп-лист.

        :param number: Номер телефона для блокировки.
        :param comment: Произвольный комментарий к записи.
        :return: JSON-ответ сервера со статусом операции.
        """
        pass

    @abstractmethod
    def del_stop_list(self, number: str) -> dict:
        """Удалить номер телефона из стоп-листа.

        :param number: Номер телефона для удаления.
        :return: JSON-ответ сервера со статусом операции.
        """
        pass

    @abstractmethod
    def callbacks(self) -> dict:
        """Получить список зарегистрированных callbacks.

        :return: JSON-ответ сервера со списком webhook-адресов.
        """
        pass

    @abstractmethod
    def add_callback(self, url: str) -> dict:
        """Добавить callback URL для уведомлений от `sms.ru`.

        :param url: Полный адрес callback/webhook.
        :return: JSON-ответ сервера со статусом операции.
        """
        pass

    @abstractmethod
    def del_callback(self, url: str) -> dict:
        """Удалить callback URL из настроек аккаунта.

        :param url: Полный адрес callback/webhook.
        :return: JSON-ответ сервера со статусом операции.
        """
        pass

    def _collect_data(self, numbers: tuple, message: str = None, multi=None,
                      from_name: str = None, ip_address: str = None,
                      timestamp: int = None, ttl: int = None, day_time: bool = False,
                      translit: bool = False, test: bool = None, debug: bool = False,
                      partner_id: int = None) -> dict:
        """Собрать и провалидировать тело запроса для SMS-методов.

        Метод используется внутренне клиентами `Client` и `AsyncClient`.
        Поддерживает два сценария:

        - общий текст сообщения через `numbers` и `message`;
        - словарь `multi` для разных текстов на разные номера.

        При использовании `numbers` каждый номер очищается от нецифровых
        символов и ведущего кода `+7` или `8`. В одном запросе разрешено не
        более 100 получателей.

        :param numbers: Кортеж номеров, переданных позиционными аргументами.
        :param message: Общий текст сообщения.
        :param multi: Словарь вида `{номер: текст}`.
        :param from_name: Имя отправителя.
        :param ip_address: IP-адрес конечного пользователя.
        :param timestamp: Unix timestamp для отложенной отправки.
        :param ttl: Срок жизни сообщения в минутах.
        :param day_time: Учитывать дневное время получателя.
        :param translit: Включить транслитерацию.
        :param test: Включить тестовый режим API.
        :param debug: Включить локальный debug-режим клиента.
        :param partner_id: Переопределить партнерский идентификатор.
        :return: Новый словарь данных, подготовленный к отправке в API.
        :raises OutOfPhoneNumbers: Если передано больше 100 получателей.
        :raises OutOfTimestamp: Если `timestamp` старше допустимого окна или
            `ttl` находится вне диапазона 1..1440.
        :raises ValueError: Если отсутствуют обязательные аргументы или IP не
            проходит проверку.
        """
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
                normalized_number = self._normalize_and_validate_phone(key)
                multi_data[f'to[{normalized_number}]'] = value
            data.update(multi_data)
        else:
            if not message:
                raise ValueError('Не указан текст сообщения')
            if not numbers:
                raise ValueError('Не указан номер(а) телефона')
            numbers = [self._normalize_and_validate_phone(i) for i in numbers]
            data.update({'to': ','.join(numbers)})
            data.update({'text': message})

        if test:
            data.update({'test': 1})
        if from_name is not None:
            data.update({'from': from_name})
        if timestamp is not None:
            max_timestamp = int(time.time()) + 5184000
            if timestamp > max_timestamp:
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

    @staticmethod
    def _normalize_phone(number: str) -> str:
        """Нормализовать номер телефона к формату API."""
        return re.sub(r'^(\+?7|8)|\D', '', number)

    @classmethod
    def _normalize_and_validate_phone(cls, number: str) -> str:
        """Нормализовать номер и проверить его базовую корректность."""
        normalized_number = cls._normalize_phone(number)
        if not normalized_number or not normalized_number.isdigit() or len(normalized_number) != 10:
            raise ValueError('Неверно указан номер телефона')
        return normalized_number
