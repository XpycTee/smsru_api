# Авторизация по звонку

API `sms.ru` позволяет подтверждать номер телефона входящим звонком. В
библиотеке это покрыто двумя методами.

## Создание проверки

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.callcheck_add("79990000000")
    print(response)
```

Типичный ответ содержит:

- `status`
- `status_code`
- `check_id`
- `call_phone`
- дополнительные представления номера для отображения

`check_id` нужно сохранить для последующей проверки статуса.

Асинхронный вариант:

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.callcheck_add("79990000000")
        print(response)

asyncio.run(main())
```

## Проверка статуса

```python
from smsru_api import Client

with Client("YOUR_API_KEY") as smsru:
    response = smsru.callcheck_status("201737-542")
    print(response)
```

Типичный ответ:

```json
{
  "status": "OK",
  "status_code": 100,
  "check_status": "401",
  "check_status_text": "Авторизация по звонку: номер подтвержден"
}
```

Асинхронный вариант:

```python
import asyncio
from smsru_api import AsyncClient

async def main():
    async with AsyncClient("YOUR_API_KEY") as smsru:
        response = await smsru.callcheck_status("201737-542")
        print(response)

asyncio.run(main())
```

## Замечания

- Для polling-проверок используйте `check_id`, возвращенный `callcheck_add()`.
- Если у вас настроены callbacks, удобнее принимать статусы на своей стороне, а
  не делать частые запросы `callcheck_status()`.
- Контекстный менеджер особенно полезен при нескольких последовательных запросах.
- Асинхронный вариант полностью повторяет синхронный API, но вызывается через
  `await`.
