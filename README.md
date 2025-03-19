<br/>
<p align="center">
  <h3 align="center">SMS.RU API</h3>

  <p align="center">
    Python API для сервиса отправки сообщений sms.ru
    <br/>
    <br/>
  </p>
</p>

![PyPI - Downloads](https://img.shields.io/pypi/dm/smsru-api) ![pypi](https://img.shields.io/pypi/v/smsru-api) ![pyversions](https://img.shields.io/pypi/pyversions/smsru-api) ![Downloads](https://img.shields.io/github/downloads/XpycTee/smsru_api/total) ![Contributors](https://img.shields.io/github/contributors/XpycTee/smsru_api?color=dark-green) ![Issues](https://img.shields.io/github/issues/XpycTee/smsru_api) ![License](https://img.shields.io/github/license/XpycTee/smsru_api) 

## Table Of Contents 

* [Built With](#built-with)
* [Getting Started](#getting-started)
    * [Installation](#installation)
* [Usage](#usage)
* [License](#license)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## Built With

- aiohttp
- certifi

## Getting Started

### Installation

```
pip install smsru-api
```

## Usage
Чтобы использовать скрипт, импортируйте класс `Client()`:

```python
from smsru_api import Client
```
Для асинхронной работы используйте класс `AsyncClient()`:
```python
from smsru_api import AsyncClient
```
Все методы асинхронного класса являются корутинами и идентичны сихронным.

Классам `Client()` или `AsyncClient()` в параметры нужно передать ваш API ключ из личного кабинета:
```python
from smsru_api import Client
from smsru_api import AsyncClient

smsru = Client('Your API KEY')
async_smsru = AsyncClient('Your API KEY')
```

#### Предыдущая реализация так же работает:
```python 
import smsru_api
# or
from smsru_api import SmsRu, AsyncSmsRu

smsru = SmsRu('api_key')
async_smsru = AsyncSmsRu('api_key')
```

### Отправка сообщений
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
Также он имеет 10 параметров:\
`numbers` * Номер телефона получателя (либо несколько номеров до 100 штук за один запрос).\
`message` * Текст сообщения в кодировке UTF-8.\
`multi` * Отправка сообщения на несколько номеров с разными текстами, если указан этот параметр, то параметры numbers и message игнорируются.\
`from_name` Имя отправителя (должно быть согласовано с администрацией).\
`ip_address` В этом параметре вы можете передать sms.ru IP адрес вашего пользователя.\
`timestamp` Время отложенной отправки.\
`ttl` Срок жизни сообщения в минутах (от 1 до 1440).\
`day_time` Учитывает часовой пояс получателя. Если указан этот параметр, то параметр time игнорируется.\
`test` Имитирует отправку сообщения для тестирования. True или False.\
`translit` Переводит все русские символы в латинские.\
`debug` Включает режим отладки. Все сообщения отправляются с параметром test: True если он не указан вручную.\
`partner_id` ID партнера. По умолчанию указан код автора, прошу если вы будете использовать мой код, не меняйте его, это то что мотивирует меня поддерживапть данное api, спасибо ツ.
### Авторизовать пользователя по звонку с его номера
Метод `callcheck_add()` добавляет телефон в ожидание на `sms.ru`:
```python
from smsru_api import Client

smsru = Client('Your API KEY')

response = smsru.callcheck_add('9XXXXXXXX0')
```
```json
{
    "status": "OK",
    "status_code": 100,
    "check_id": "201737-542",
    "call_phone": "78005008275",
    "call_phone_pretty": "+7 (800) 500-8275",
    "call_phone_html": "&lt;a href="callto:78005008275"&gt;+7 (800) 500-8275&lt;\a&gt;"
}
```
Метод возвращает `JSON` ответ, полученный от `sms.ru`.
Также он имеет 1 параметр:\
`phone` * Номер телефона пользователя, который необходимо авторизовать (с которого мы будем ожидать звонок).
### Проверка статуса звонка
Метод `callcheck_status()` проверяет, был ли совершен звонок от пользователя.

> `sms.ru` настоятельно рекомендует использовать бесплатную опцию API callback для более быстрого и удобного получения статусов проверок. Она позволяет вам не запрашивать многократно статус проверки - он будет автоматически отправляться на ваш сервер в реальном времени.

```python
from smsru_api import Client

smsru = Client('Your API KEY')

response = smsru.callcheck_status('201737-542')
```
```json
{
    "status": "OK",
    "status_code": 100,
    "check_status": "401",
    "check_status_text": "Авторизация по звонку: номер подтвержден"
}
```
Метод возвращает `JSON` ответ, полученный от `sms.ru`.
Также он имеет 1 параметр:\
`check_id` * Идентификатор авторизации, полученный от `sms.ru` при добавлении номера.
### Получить статус отправленных сообщений
Метод `status()` узнает статус СМС по его `sms_id`:
```python
from smsru_api import Client

smsru = Client('Your API KEY')

response = smsru.status('1000-100000')
```
```json
{
    "status": "OK",
    "status_code": 100,
    "sms": {
        "1000-100000": {
            "status": "OK",
            "status_code": 102,
            "status_text": "Сообщение отправлено (в пути)", 
            "cost": "X.XX", 
            "send_time": 1651453200, 
            "status_time": 1651453200    
        }
}
```
### Узнать стоимость СМС сообщений
Метод `cost()` запрашивает у сервера стоимость СМС:
```python
from smsru_api import Client

smsru = Client('Your API KEY')

response = smsru.cost('9XXXXXXXX0', '9XXXXXXXX1', message='Message to sms')
```
```json
{
    "status": "OK",
    "status_code": 100,
    "sms": {
        "9XXXXXXXXX":  {
            "status": "OK", 
            "status_code": 100, 
            "cost": 0, 
            "sms": 1
        }
    }, 
    "total_cost": 0, 
    "total_sms": 1
}
```
### Узнать баланс
Метод `balance()` запрашивает у сервера баланс аккаунта:
```python
from smsru_api import Client

smsru = Client('Your API KEY')

response = smsru.balance()
```
```json
{
    "status": "OK",
    "status_code": 100,
    "balance": 0
}
```
### Узнать лимит
Метод `limit()` запрашивает у сервера лимиты по отправке СМС.\
Метод `free()` запрашивает у сервера бесплатные лимиты по отправке СМС:
```python
from smsru_api import Client

smsru = Client('Your API KEY')

response = smsru.limit()
free_response = smsru.free()
```
```json
{
    "status": "OK",
    "status_code": 100,
    "total_limit": 5000,
    "used_today": 50
}

{
    "status": "OK",
    "status_code": 100,
    "total_free": 5,
    "used_today": null
}
```
### Получить одобренных отправителей
Метод `senders()` запрашивает у сервера отправителей:
```python
from smsru_api import Client

smsru = Client('Your API KEY')

response = smsru.senders()
```
```json
{
    "status": "OK",
    "status_code": 100,
    "senders": ["company.com", "Company"]
}
```
### Добавить номер в стоп-лист
Метод `add_stop_list()` добавляет номер в стоп-лист:
```python
from smsru_api import Client
smsru = Client('Your API KEY')

response = smsru.add_stop_list('9XXXXXXXXX', 'Comment')
```
```json
{
    "status": "OK",
    "status_code": 100
}
```
### Удалить номер из стоп-листа
Метод `del_stop_list()` удаляет номер из стоп-листа:
```python
from smsru_api import Client
smsru = Client('Your API KEY')

response = smsru.del_stop_list('9XXXXXXXXX')
```
```json
{
    "status": "OK",
    "status_code": 100
}
```
### Получить список номеров в стоп-листе
Метод `stop_list()` получает список номеров в стоп-листе:
```python
from smsru_api import Client
smsru = Client('Your API KEY')

response = smsru.stop_list()
```
```json
{
    "status": "OK",
    "status_code": 100,
    "stoplist": {
        "9XXXXXXXXX": "Comment",
        "9XXXXXXXX1": "Comment"
    }
}
```
### Добавить callback (webhook)
Метод `add_callback()` добавляет callback (webhook) на аккаунт:
```python
from smsru_api import Client
smsru = Client('Your API KEY')

response = smsru.add_callback('https://campany.com/callback')
```
```json
{
    "status": "OK",
    "status_code": 100,
    "callback": [
        "https://campany.com/callback",
        "http://anothersite.ru/callback/index.php"
    ]
 }
```
### Удалить callback (webhook)
Метод `del_callback()` удаляет callback (webhook) из аккаунта:
```python
from smsru_api import Client
smsru = Client('Your API KEY')

response = smsru.del_callback('https://campany.com/callback')
```
```json
 {
    "status": "OK",
    "status_code": 100,
    "callback": [
        "http://anothersite.ru/callback/index.php"
    ]
 }
```
### Получить список callbacks (webhooks)
Метод `callbacks()` получает список callbacks (webhooks):
```python
from smsru_api import Client
smsru = Client('Your API KEY')

response = smsru.callbacks()
```
```json
 {
    "status": "OK",
    "status_code": 100,
    "callback": [
        "https://campany.com/callback",
        "http://anothersite.ru/callback/index.php"
    ]
}
```

## License

Distributed under the Apache-2.0 License. See [LICENSE](https://github.com/XpycTee/smsru_api/blob/main/LICENSE.md) for more information.

## Authors

* **XpycTee** - *просто я* - [XpycTee](https://github.com/XpycTee) - *smsru_api*

## Acknowledgements

* [XpycTee](https://github.com/XpycTee)
