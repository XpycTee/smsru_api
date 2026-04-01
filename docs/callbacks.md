# Callbacks и webhooks

`sms.ru` позволяет отправлять уведомления на ваш сервер через callback URL.

## Получить список callback URL

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.callbacks()
    print(response)
```

Асинхронный вариант:

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.callbacks()
        print(response)

asyncio.run(main())
```

## Добавить callback URL

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.add_callback("https://example.com/smsru/callback")
    print(response)
```

Асинхронный вариант:

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.add_callback("https://example.com/smsru/callback")
        print(response)

asyncio.run(main())
```

## Удалить callback URL

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.del_callback("https://example.com/smsru/callback")
    print(response)
```

Асинхронный вариант:

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.del_callback("https://example.com/smsru/callback")
        print(response)

asyncio.run(main())
```

- Используйте HTTPS URL, доступный извне.
- Если callback уже настроен, он может быть удобнее polling-запросов к
  `status()` и `callcheck_status()`.
- Контекстный менеджер гарантирует корректное управление соединением при
  нескольких последовательных операциях с callbacks.
- В асинхронном коде используйте те же методы через `await`.
