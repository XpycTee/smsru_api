# Синхронные и асинхронные примеры

Библиотека поддерживает одинаковый набор методов в sync и async вариантах.

## Синхронный код

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")

balance = smsru.balance()
cost = smsru.cost("79990000000", message="Тест")
message = smsru.send("79990000000", message="Привет", debug=True)
```

## Асинхронный код

```python
import asyncio

from smsru_api import AsyncClient


async def main():
    smsru = AsyncClient("YOUR_API_KEY")
    balance = await smsru.balance()
    cost = await smsru.cost("79990000000", message="Тест")
    message = await smsru.send("79990000000", message="Привет", debug=True)
    return balance, cost, message


asyncio.run(main())
```

## Как выбрать клиент

- Используйте `Client`, если проект уже синхронный и дополнительная
  асинхронность не нужна.
- Используйте `AsyncClient`, если проект построен на `asyncio`, FastAPI,
  aiohttp или другом асинхронном стеке.

## Обратная совместимость

Если у вас остался код старых версий, можно продолжать использовать алиасы:

```python
from smsru_api import SmsRu, AsyncSmsRu

smsru = SmsRu("YOUR_API_KEY")
async_smsru = AsyncSmsRu("YOUR_API_KEY")
```
