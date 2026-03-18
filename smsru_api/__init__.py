"""Публичный API пакета `smsru_api`.

Экспортирует синхронный и асинхронный клиенты, алиасы для обратной
совместимости и публичные исключения библиотеки.
"""

from .client import Client as SmsRu
from .aioclient import AsyncClient as AsyncSmsRu
from .client import Client
from .aioclient import AsyncClient
from .template import OutOfPhoneNumbers, OutOfTimestamp

__all__ = [
    "Client",
    "AsyncClient",
    "SmsRu",
    "AsyncSmsRu",
    "OutOfPhoneNumbers",
    "OutOfTimestamp",
]
