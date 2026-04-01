# Баланс и лимиты

Эти методы помогают получить служебную информацию об аккаунте `sms.ru`.

## Баланс

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.balance()
    print(response)
```

Используйте метод, чтобы получить текущий остаток средств.

Асинхронный вариант:

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.balance()
        print(response)

asyncio.run(main())
```

## Лимиты

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.limit()
    print(response)
```

Метод возвращает информацию о доступных лимитах аккаунта.

Асинхронный вариант:

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.limit()
        print(response)

asyncio.run(main())
```

## Бесплатный лимит

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.free()
    print(response)
```

Используется для получения сведений о бесплатных сообщениях или лимитах, если
они поддерживаются вашим тарифом.

Асинхронный вариант:

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.free()
        print(response)

asyncio.run(main())
```

## Одобренные отправители

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.senders()
    print(response)
```

Метод возвращает список имен отправителя, одобренных в аккаунте.

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.senders()
        print(response)

asyncio.run(main())
```
