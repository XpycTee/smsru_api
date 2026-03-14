# Callbacks и webhooks

`sms.ru` позволяет отправлять уведомления на ваш сервер через callback URL.

## Получить список callback URL

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.callbacks()
```

## Добавить callback URL

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.add_callback("https://example.com/smsru/callback")
```

## Удалить callback URL

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.del_callback("https://example.com/smsru/callback")
```

## Практические рекомендации

- Используйте HTTPS URL, доступный извне.
- Если callback уже настроен, он может быть удобнее polling-запросов к
  `status()` и `callcheck_status()`.
- В асинхронном коде используйте те же методы через `await`.
