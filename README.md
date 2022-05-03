# sms ru api python
 Python API для сервиса отправки сообщений sms.ru
# Установка
```
pip install smsru-api
```
# Использование
Чтобы использовать скрипт просто импортируйте его в свой код
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
# Отправка сообщений
Метод `send()` отправляет ваше сообщение на номер(а) через `sms.ru`
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.send(['9XXXXXXXXX'], 'Message to sms')

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
#    "sms": {
#        "79XXXXXXXXX": {
#            "status": "OK", // Возможные варианты: OK или ERROR.
#            "status_code": 100, // Успешный код выполнения, сообщение принято на отправку
#            "sms_id": "000000-10000000" // ID сообщения
#        },
#        "79XXXXXXXXX": {
#            "status": "ERROR",
#            "status_code": 207, // Код ошибки
#            "status_text": "На этот номер (или один из номеров) нельзя отправлять сообщения, либо указано более 100 номеров в списке получателей" // Описание ошибки
#        }
#    } ,
#    "balance": XXXX.XX // Ваш баланс после отправки
```
Метод возврощает `JSON` ответ полученый от `sms.ru`
также он имеет 10 параметров:
Параметр | Обязательно | Описание
---------|-------------|-----------------------
numbers| + | Номер телефона получателя (либо несколько номеров до 100 штук за один запрос). Номер телефона для отправки сообщения, желатьельно без кода страны. Возможно использование и других видов, скрипт удалит все не нужное.
message| + | Текст сообщения в кодировке UTF-8 .
from_name| - | Имя отправителя (должно быть согласовано с администрацией).
ip_address| - | В этом параметре вы можете передать нам  IP адрес вашего пользователя.
timestamp| - | Время отложенной отправки.
ttl| - | Срок жизни сообщения в минутах (от 1 до 1440).
day_time| - | Учитывает часовой пояс получателя. Если указан этот параметр, то параметр time игнорируется.
test| - | Имитирует отправку сообщения для тестирования. True или False
translit| - | Переводит все русские символы в латинские.
debug| - | Включает режим отладки. Все собщения отправляются с парпметром test: True если он не указан в ручную
# Отправить четырехзначный авторизационный код звонком
Метод `call()` отправляет запрос на звонок по указанному номеру
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.call('9XXXXXXXXX')

### response:
# {
#     "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#     "code": "1435", // Последние 4 цифры номера, с которого мы совершим звонок пользователю
#     "call_id": "000000-10000000", // ID звонка
#     "cost": 0.4, // Стоимость звонка
#     "balance": XXXX.XX // Ваш баланс после совершения звонка
# }
```
# Получить статус отправленных сообщений
Метод `status()` узнает статус СМС по его `sms_id`
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.status('1000-100000')

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
#    "sms": {
#        "1000-100000": {
#            "status": "OK", // Возможные варианты: OK или ERROR.
#            "status_code": 102, // Успешный код выполнения
#            "status_text": 'Сообщение отправлено (в пути)', 
#            "cost": 'X.XX', 
#            "send_time": 1651453200, 
#            "status_time": 1651453200    
#        }
# }
```
# Узнать стоимость СМС сообщений
Метод `cost()` запрашивает у сервера стоимость СМС
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.cost(['9XXXXXXXXX'], 'Message to sms')

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
#    "sms": {
#        "9XXXXXXXXX":  {
#            "status": "OK", 
#            "status_code": 100, 
#            "cost": X.X, 
#            "sms": 1
#        }
#    }, 
#    "total_cost": X.X, 
#    "total_sms": 1
# }
```
# Узнать баланс
Метод `balance()` запрашивает у сервера баланс аккаунта
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.balance()

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
#    "balance": XXXX.XX
# }
```
# Узнать лимит
Метод `limit()` запрашивает у сервера лимты по отправке СМС \
Метод `free()` запрашивает у сервера беспатные лимты по отправке СМС
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.limit()
free_response = sms_ru.free()

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
#    "total_limit": 5000,
#    "used_today": 50
# }
### free_response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
#    "total_free": 5,
#    "used_today": None
# }
```
# Получить одобренных отправителей
Метод `senders()` запрашивает у сервера отправителей
```python
from smsru_api import SmsRu

sms_ru = SmsRu('Your API KEY')

response = sms_ru.senders()

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
#    "senders": ["company.com", "Company"]
# }
```
# Добавить номер в стоплист
Метод `add_stop_list()` добавляет номер в стоп лист
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.add_stop_list('9XXXXXXXXX', 'Comment')

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
# }
```
# Удалить номер из стоплиста
Метод `del_stop_list()` удаляет номер из стоп листа
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.del_stop_list('9XXXXXXXXX')

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
# }
```
# Получить список номеров в стоплисте
Метод `stop_list()` получает список номеров в стоп листе
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.stop_list()

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
#    "stoplist": {
#        "9XXXXXXXXX": "Comment",
#        "9XXXXXXXX1": "Comment"
#    }
# }
```
# Добавить webhook
Метод `add_callback()` добавляет webhook (callback) на аккаунт
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.add_callback('https://campany.com/callback')

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
#    "callback": [ // Список добавленных callback
#         "https://campany.com/callback", // первый сайт
#         "http://anothersite.ru/callback/index.php" // второй сайт
#    ]
# }
```
# Удалить webhook
Метод `del_callback()` удаляет webhook (callback) из аккаунта
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.del_callback('https://campany.com/callback')

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
#    "callback": [ // Список добавленных callback
#         "http://anothersite.ru/callback/index.php"
#    ]
# }
```
# Получить список вебхуков (callbacks)
Метод `callbacks()` получает список вебхуков (callbacks)
```python
from smsru_api import SmsRu
sms_ru = SmsRu('Your API KEY')

response = sms_ru.callbacks()

### response:
# {
#    "status": "OK", // Запрос выполнен успешно (нет ошибок в авторизации, проблем с отправителем, итд...)
#    "status_code": 100, // Успешный код выполнения
#    "callback": [ // Список добавленных callback
#         "https://campany.com/callback", // первый сайт
#         "http://anothersite.ru/callback/index.php" // второй сайт
#    ]
# }
```