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

aiohttp

## Getting Started


### Installation

```
pip install smsru-api
```

## Usage

Чтобы использовать скрипт, просто импортируйте его в свой код
```python
import smsru_api
```
или импортируйте сам класс `SmsRu()`
```python
from smsru_api import SmsRu
```
Для асинхронной работы есть класс `AsyncSmsRu()`

```python
from smsru_api import AsyncSmsRu
```
Все методы асинхронного класса это корутины.

Классам `SmsRu()` или `AsyncSmsRu()` в параметры нужно передать ваш API ключ из личного кабинета
```python
from smsru_api import SmsRu, AsyncSmsRu

sms_ru = SmsRu('Your API KEY')
async_sms_ru = AsyncSmsRu('Your API KEY')
```
#### Отправка сообщений
Метод `send()` отправляет ваше сообщение на номер(а) через `sms.ru`
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.send('9XXXXXXXX0', '9XXXXXXXX1', message='Message to sms')
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
            "status_text": "На этот номер (или один из номеров) нельзя отправлять сообщения, либо указано более 100 номеров в списке получателей" // Описание ошибки
        }
    } ,
    "balance": 0
}
```
Метод возвращает `JSON` ответ полученный от `sms.ru`
также он имеет 10 параметров:\
`numbers` * Номер телефона получателя (либо несколько номеров до 100 штук за один запрос).\
`message` * Текст сообщения в кодировке UTF-8.\
`from_name` Имя отправителя (должно быть согласовано с администрацией).\
`ip_address` В этом параметре вы можете передать нам IP адрес вашего пользователя.\
`timestamp` Время отложенной отправки.\
`ttl` Срок жизни сообщения в минутах (от 1 до 1440).\
`day_time` Учитывает часовой пояс получателя. Если указан этот параметр, то параметр time игнорируется.\
`test` Имитирует отправку сообщения для тестирования. True или False\
`translit` Переводит все русские символы в латинские.\
`debug` Включает режим отладки. Все сообщения отправляются с параметром test: True если он не указан в ручную
#### Получить статус отправленных сообщений
Метод `status()` узнает статус СМС по его `sms_id`
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.status('1000-100000')
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
#### Узнать стоимость СМС сообщений
Метод `cost()` запрашивает у сервера стоимость СМС
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.cost('9XXXXXXXX0', '9XXXXXXXX1', message='Message to sms')
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
#### Узнать баланс
Метод `balance()` запрашивает у сервера баланс аккаунта
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.balance()
```
```json
{
    "status": "OK",
    "status_code": 100,
    "balance": 0
}
```
#### Узнать лимит
Метод `limit()` запрашивает у сервера лимиты по отправке СМС \
Метод `free()` запрашивает у сервера бесплатные лимиты по отправке СМС
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.limit()
free_response = sms_ru.free()
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
#### Получить одобренных отправителей
Метод `senders()` запрашивает у сервера отправителей
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.senders()
```
```json
{
    "status": "OK",
    "status_code": 100,
    "senders": ["company.com", "Company"]
}
```
#### Добавить номер в стоп лист
Метод `add_stop_list()` добавляет номер в стоп лист
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.add_stop_list('9XXXXXXXXX', 'Comment')
```
```json
{
    "status": "OK",
    "status_code": 100
}
```
#### Удалить номер из стоп листа
Метод `del_stop_list()` удаляет номер из стоп листа
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.del_stop_list('9XXXXXXXXX')
```
```json
{
    "status": "OK",
    "status_code": 100
}
```
#### Получить список номеров в стоп листе
Метод `stop_list()` получает список номеров в стоп листе
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.stop_list()
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
#### Добавить callback (webhook)
Метод `add_callback()` добавляет callback (webhook) на аккаунт
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.add_callback('https://campany.com/callback')
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
#### Удалить callback (webhook)
Метод `del_callback()` удаляет callback (webhook) из аккаунта
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.del_callback('https://campany.com/callback')
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
#### Получить список callbacks (webhooks)
Метод `callbacks()` получает список callbacks (webhooks)
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.callbacks()
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
