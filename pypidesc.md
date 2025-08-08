<p align="center">
  <h3 align="center">SMS.RU API</h3>
  <p align="center">
    [A]sync Python API для сервиса отправки сообщений sms.ru
  </p>
</p>

![PyPI - Downloads](https://img.shields.io/pypi/dm/smsru-api?label=PyPI%20Downloads) ![pypi](https://img.shields.io/pypi/v/smsru-api?label=PyPI%20Release)

Python Versions\
![pyversions](https://img.shields.io/pypi/pyversions/smsru-api?label=Python) 

License\
![License](https://img.shields.io/github/license/XpycTee/smsru_api?label=License) 



## Начало работы

### Установка

Для установки библиотеки используйте pip:

```sh
pip install smsru-api
```

### Использование

> Подробную документацию по пакету ищите на [GitHub Wiki](https://github.com/XpycTee/smsru_api/wiki)

Чтобы начать использовать библиотеку, импортируйте класс `Client`:

```python
from smsru_api import Client
```

Создайте экземпляр класса, передав ваш API ключ:

```python
smsru = Client('Your API KEY')
```

Теперь вы можете использовать методы класса для отправки сообщений и выполнения других операций с API `sms.ru`.

```python
from smsru_api import Client
```
Для асинхронной работы используйте класс `AsyncClient()`:
```python
from smsru_api import AsyncClient
```
> Все методы асинхронного класса являются корутинами и идентичны синхронным.

Классам `Client()` или `AsyncClient()` в параметры нужно передать ваш API ключ из личного кабинета:
```python
from smsru_api import Client
from smsru_api import AsyncClient

smsru = Client('Your API KEY')
async_smsru = AsyncClient('Your API KEY')
```

**Старая реализация так же работает:**
```python 
from smsru_api import SmsRu, AsyncSmsRu

smsru = SmsRu('api_key')
async_smsru = AsyncSmsRu('api_key')
```

## Отправка сообщений
Метод `send()` отправляет ваше сообщение на номер(а) через `sms.ru`

Отправить один текст на один или несколько номеров, указанных через запятую:
```python
from smsru_api import Client

smsru = Client('Your API KEY')

response = smsru.send('9XXXXXXXX0', '9XXXXXXXX1', message='Message to sms')
```
Отправить разный текст на разные номера:
```python
from smsru_api import Client

smsru = Client('Your API KEY')

multi_dict = {
    '9XXXXXXXX0': 'Message to sms', 
    '9XXXXXXXX1': 'Another message to sms'
}

response = smsru.send(multi=multi_dict)
```
**Ответ от сервера:**
```json
{
    "status": "OK",
    "status_code": 100,
    "sms": {
        "79XXXXXXXX0": {
            "status": "OK",
            "status_code": 100,
            "sms_id": "000000-10000000"
        },
        "79XXXXXXXX1": {
            "status": "ERROR",
            "status_code": 207,
            "status_text": "На этот номер (или один из номеров) нельзя отправлять сообщения, либо указано более 100 номеров в списке получателей"
        }
    } ,
    "balance": 0
}
```
Метод возвращает `JSON` ответ, полученный от `sms.ru`.
Также он имеет 10 параметров:

- `numbers`: Номер телефона получателя (либо несколько номеров до 100 штук за один запрос).
- `message`: Текст сообщения в кодировке UTF-8.
- `multi`: Отправка сообщения на несколько номеров с разными текстами. Если указан этот параметр, то параметры `numbers` и `message` игнорируются.
- `from_name`: Имя отправителя (должно быть согласовано с администрацией).
- `ip_address`: IP адрес вашего пользователя.
- `timestamp`: Время отложенной отправки.
- `ttl`: Срок жизни сообщения в минутах (от 1 до 1440).
- `day_time`: Учитывает часовой пояс получателя. Если указан этот параметр, то параметр `time` игнорируется.
- `test`: Имитирует отправку сообщения для тестирования. `True` или `False`.
- `translit`: Переводит все русские символы в латинские.
- `debug`: Включает режим отладки. Все сообщения отправляются с параметром `test: True`, если он не указан вручную.
- `partner_id`: ID партнера. По умолчанию указан код автора. Прошу, если вы будете использовать мой код, не меняйте его. Это то, что мотивирует меня поддерживать данный API, спасибо ツ.

## Лицензия

Распространяется по лицензии Apache-2.0. См. [LICENSE](https://github.com/XpycTee/smsru_api/blob/main/LICENSE.md) для получения дополнительной информации.

## Авторы

* **XpycTee** - *просто я* - [XpycTee](https://github.com/XpycTee) - *smsru_api*
