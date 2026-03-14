# Стоп-лист

Стоп-лист позволяет запретить отправку сообщений на определенные номера.

## Получить текущий список

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.stop_list()
```

## Добавить номер

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.add_stop_list("79990000000", comment="Отписка пользователя")
```

Перед отправкой номера библиотека очищает его от нецифровых символов и
удаляет ведущий код `+7` или `8`.

## Удалить номер

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.del_stop_list("79990000000")
```

Асинхронный клиент использует те же методы с `await`.
