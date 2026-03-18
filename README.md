<p align="center">
  <h3 align="center">SMS.RU API</h3>
  <p align="center">
    Синхронный и асинхронный Python API для сервиса отправки сообщений sms.ru
  </p>
</p>

Python Versions\
![pyversions](https://img.shields.io/pypi/pyversions/smsru-api?label=Python)

PyPI\
![PyPI - Downloads](https://img.shields.io/pypi/dm/smsru-api?label=PyPI%20Downloads) ![pypi](https://img.shields.io/pypi/v/smsru-api?label=PyPI%20Release)

GitHub\
![Downloads](https://img.shields.io/github/downloads/XpycTee/smsru_api/total?label=GitHub%20Downloads) ![GitHub Release](https://img.shields.io/github/v/release/xpyctee/smsru_api?label=GitHub%20Release) ![Contributors](https://img.shields.io/github/contributors/XpycTee/smsru_api?color=dark-green&label=Contributors) ![Issues](https://img.shields.io/github/issues/XpycTee/smsru_api?label=Issues)

License\
![License](https://img.shields.io/github/license/XpycTee/smsru_api?label=License)

## О проекте

`smsru_api` предоставляет два клиента для работы с HTTP API `sms.ru`:

- `Client` для синхронного кода
- `AsyncClient` для `asyncio`

Поддерживаются отправка SMS, расчет стоимости, проверка статуса, авторизация по
звонку, работа со стоп-листом, callback URL и сервисные методы аккаунта.

Подробное руководство теперь хранится прямо в репозитории:

- [Локальная документация `docs/`](docs/README.md)

## Установка

```sh
pip install smsru-api
```

## Быстрый старт

### Синхронный клиент

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")

response = smsru.send("79990000000", message="Привет от sms.ru", debug=True)
print(response)
```

Для обратной совместимости этот сценарий остается `one-shot`: на каждый
запрос создается временный HTTP-клиент, поэтому ручное закрытие не требуется.

Если нужно переиспользовать соединение для нескольких запросов подряд,
используйте контекстный менеджер:

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    balance = smsru.balance()
    limit = smsru.limit()
```

### Асинхронный клиент

```python
import asyncio

from smsru_api import AsyncClient


async def main():
    smsru = AsyncClient("YOUR_API_KEY")
    response = await smsru.balance()
    print(response)


asyncio.run(main())
```

Асинхронный клиент тоже сохраняет прежнее поведение без `async with`: каждый
запрос выполняется через временный `httpx.AsyncClient`.

Для переиспользования соединения в рамках нескольких запросов:

```python
import asyncio

from smsru_api import AsyncClient


async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        balance = await smsru.balance()
        limit = await smsru.limit()
        return balance, limit


asyncio.run(main())
```

### Обратная совместимость

Сохраняются алиасы старого API:

```python
from smsru_api import SmsRu, AsyncSmsRu

smsru = SmsRu("YOUR_API_KEY")
async_smsru = AsyncSmsRu("YOUR_API_KEY")
```

## Отправка SMS

Отправить один и тот же текст на несколько номеров:

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.send(
    "79990000000",
    "79990000001",
    message="Код подтверждения: 1234",
)
```

Отправить разные тексты на разные номера через `multi`:

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.send(
    multi={
        "79990000000": "Код подтверждения: 1234",
        "79990000001": "Код подтверждения: 5678",
    }
)
```

Дополнительные параметры `send()`:

- `from_name` — имя отправителя, согласованное с администрацией
- `ip_address` — IP-адрес конечного пользователя
- `timestamp` — Unix timestamp для отложенной отправки
- `ttl` — срок жизни сообщения в минутах, от `1` до `1440`
- `day_time` — учитывать локальное дневное время получателя
- `test` — тестовый режим API
- `debug` — локальный режим отладки; если `test` не указан, включает `test`
- `translit` — транслитерация текста
- `partner_id` — переопределение партнерского идентификатора

Ограничения и особенности:

- за один запрос можно передать не более 100 получателей
- при использовании `multi` параметры `numbers` и `message` игнорируются
- номера очищаются от нецифровых символов и от ведущего `+7` или `8`
- после нормализации номер должен оставаться корректным 10-значным значением,
  иначе библиотека выбросит `ValueError`
- ключи `multi` тоже нормализуются; если два ключа схлопываются в один номер,
  библиотека выбросит `ValueError`
- при некорректных лимитах или времени библиотека выбрасывает
  `OutOfPhoneNumbers` и `OutOfTimestamp`

## Публичный API

### Сообщения

- `send(...)` — отправка SMS
- `cost(*numbers, message=...)` — расчет стоимости
- `status(sms_id)` — статус сообщения

### Авторизация по звонку

- `callcheck_add(phone)` — создать проверку
- `callcheck_status(check_id)` — узнать статус проверки

### Аккаунт

- `balance()` — баланс аккаунта
- `limit()` — лимиты аккаунта
- `free()` — бесплатный лимит
- `senders()` — список одобренных отправителей

### Стоп-лист

- `stop_list()` — получить текущий список
- `add_stop_list(number, comment="")` — добавить номер
- `del_stop_list(number)` — удалить номер

### Callback URL

- `callbacks()` — список callback URL
- `add_callback(url)` — добавить callback URL
- `del_callback(url)` — удалить callback URL

## Структура документации

- [CHANGELOG.md](CHANGELOG.md) — заметки по релизам и user-facing изменениям
- [README.md](README.md) — быстрый старт и обзор API
- [docs/README.md](docs/README.md) — подробная документация по возможностям
- [pypidesc.md](pypidesc.md) — краткое описание для PyPI
- docstring'и в коде — справка по параметрам и ограничениям в IDE

## Тесты

Для локальной разработки:

```sh
pip install -e ".[test]"
pytest
```

Обычный `pytest` запускает только unit-тесты. Live-проверки вынесены в
отдельный opt-in сценарий и требуют переменные окружения:

- `SMSRU_API_ID`
- `SMSRU_TEST_PHONE`
- `AUTO_TEST=true` — опционально, чтобы пропустить сценарии `callcheck_*`
- `SMSRU_LOAD_DOTENV=true` — опционально, чтобы подгрузить значения из `.env`

Явный запуск live-тестов:

```sh
pytest tests/test_live.py -m live
```

Если установлен `python-dotenv`, live-тесты смогут подгрузить значения из
локального `.env`, но только при `SMSRU_LOAD_DOTENV=true`.

## Подробная документация

В каталоге [`docs/`](docs/README.md) собраны отдельные страницы:

- [Обзор API](docs/api-overview.md)
- [Отправка сообщений](docs/messages.md)
- [Авторизация по звонку](docs/callcheck.md)
- [Баланс и лимиты](docs/account.md)
- [Стоп-лист](docs/stoplist.md)
- [Callbacks и webhooks](docs/callbacks.md)
- [Синхронные и асинхронные примеры](docs/sync-async.md)

## Лицензия

Проект распространяется по лицензии Apache-2.0. Подробности в [LICENSE](LICENSE).

## Ссылки

- GitHub: [smsru_api](https://github.com/XpycTee/smsru_api)
- PyPI: [smsru-api](https://pypi.org/project/smsru-api/)
