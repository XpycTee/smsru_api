# Синхронные и асинхронные примеры

Библиотека поддерживает одинаковый набор методов в sync и async вариантах.

## Синхронный код

Рекомендуемый подход — использовать контекстный менеджер для переиспользования
соединения:

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    balance = smsru.balance()
    cost = smsru.cost("79990000000", message="Тест")
    message = smsru.send("79990000000", message="Привет", debug=True)
```

Обычный sync-вызов обратно совместим: каждый запрос создает временный
HTTP-клиент.


## Асинхронный код

Используйте `async with` для корректного управления соединением:

```python
import asyncio

from smsru_api import AsyncClient


async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        balance = await smsru.balance()
        cost = await smsru.cost("79990000000", message="Тест")
        message = await smsru.send("79990000000", message="Привет", debug=True)
        return balance, cost, message


asyncio.run(main())
```

Без `async with` поведение остается совместимым: на каждый запрос создается
временный HTTP-клиент.

## Вспомогательный пример: один запрос напрямую

Если нужно сделать один запрос и больше ничего не делать, можно обойтись
без менеджера. В этом случае важно явно закрыть ресурсы:

```python
from smsru_api import Client

# Синхронный вариант
smsru = Client("YOUR_API_KEY")
balance = smsru.balance()

# Закрычем соединение (рекомендуется)
smsru.close()

# Асинхронный вариант
import asyncio
async def get_balance():
    smsru = AsyncClient("YOUR_API_KEY")
    balance = await smsru.balance()
    await smsru.aclose()  # Закрываем асинхронное соединение
    return balance

asyncio.run(get_balance())
```

> **Рекомендация**: Для нескольких операций подряд используйте контекстный менеджер
> (`with`/`async with`) — это безопаснее и гарантирует закрытие ресурсов.

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

## Публичные исключения

Если нужно обрабатывать лимиты получателей или некорректные временные
параметры, импортируйте исключения из корня пакета:

```python
from smsru_api import OutOfPhoneNumbers, OutOfTimestamp
```
