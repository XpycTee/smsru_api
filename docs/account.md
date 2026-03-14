# Баланс и лимиты

Эти методы помогают получить служебную информацию об аккаунте `sms.ru`.

## Баланс

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.balance()
```

Используйте метод, чтобы получить текущий остаток средств.

## Лимиты

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.limit()
```

Метод возвращает информацию о доступных лимитах аккаунта.

## Бесплатный лимит

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.free()
```

Используется для получения сведений о бесплатных сообщениях или лимитах, если
они поддерживаются вашим тарифом.

## Одобренные отправители

```python
from smsru_api import Client

smsru = Client("YOUR_API_KEY")
response = smsru.senders()
```

Метод возвращает список имен отправителя, одобренных в аккаунте.
