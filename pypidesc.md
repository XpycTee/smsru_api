<p align="center">
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/images/dark-mode.svg">
        <source media="(prefers-color-scheme: light)" srcset="docs/images/light-mode.svg">
    <img alt="Описание изображения" src="docs/images/light-mode.svg" width="250">
    </picture>
    <!--h3 align="center">SMS.RU API</h3-->
    <p align="center">
        Синхронный и асинхронный Python API для сервиса отправки сообщений sms.ru
    </p>
</p>

[![PyPI Downloads](https://img.shields.io/pepy/dt/smsru-api?style=for-the-badge)](https://pypi.org/project/smsru-api/) 
[![pypi](https://img.shields.io/pypi/v/smsru-api?label=PyPI%20Release&style=for-the-badge)](https://pypi.org/project/smsru-api/) 

Python Versions\
![pyversions](https://img.shields.io/pypi/pyversions/smsru-api?label=Python&style=for-the-badge)

License\
[![License](https://img.shields.io/github/license/XpycTee/smsru_api?label=License&style=for-the-badge)](https://github.com/XpycTee/smsru_api/blob/main/LICENSE)

## Кратко

`smsru_api` предоставляет:

- `Client` для синхронной работы с API `sms.ru`
- `AsyncClient` для асинхронного кода
- обратную совместимость через `SmsRu` и `AsyncSmsRu`

Библиотека покрывает:

- отправку SMS через `send()`
- расчет стоимости через `cost()`
- проверку статуса через `status()`
- авторизацию по звонку через `callcheck_add()` и `callcheck_status()`
- методы аккаунта `balance()`, `limit()`, `free()`, `senders()`
- стоп-лист и callback URL

## Установка

```sh
pip install smsru-api
```

## Быстрый старт

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.send("79990000000", message="Привет от sms.ru", debug=True)
print(response)
```

Асинхронный вариант:

```python
from smsru_api import AsyncClient

smsru = AsyncClient("YOUR_API_KEY")
response = await smsru.balance()
```

## Важные особенности

- можно передавать один текст на несколько номеров или словарь `multi`
- за один запрос допускается не более 100 получателей
- номера очищаются от нецифровых символов и ведущего `+7` или `8`
- `debug=True` включает тестовый режим, если `test` не указан явно
- `ttl` должен быть в диапазоне от `1` до `1440`

## Подробная документация

Подробное руководство хранится в репозитории:

- [README.md](https://github.com/XpycTee/smsru_api/blob/main/README.md) — быстрый старт
- [docs/README.md](https://github.com/XpycTee/smsru_api/blob/main/docs/README.md) — полная документация

## Ссылки

- GitHub: [smsru_api](https://github.com/XpycTee/smsru_api)
- PyPI: [smsru-api](https://pypi.org/project/smsru-api/)
