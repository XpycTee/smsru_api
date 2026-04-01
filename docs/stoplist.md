# Стоп-лист

Стоп-лист позволяет запретить отправку сообщений на определенные номера.

## Получить текущий список

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.stop_list()
    print(response)
```

Асинхронный вариант:

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.stop_list()
        print(response)

asyncio.run(main())
```

## Добавить номер

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.add_stop_list("79990000000", comment="Отписка пользователя")
    print(response)
```

Перед отправкой номера библиотека очищает его от нецифровых символов,
удаляет ведущий код `+7` или `8` и затем проверяет, что результат содержит
корректный 10-значный номер. Иначе будет выброшен `ValueError`.

Асинхронный вариант:

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.add_stop_list("79990000000", comment="Отписка пользователя")
        print(response)

asyncio.run(main())
```

## Удалить номер

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.del_stop_list("79990000000")
    print(response)
```

Асинхронный вариант:

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.del_stop_list("79990000000")
        print(response)

asyncio.run(main())
```
