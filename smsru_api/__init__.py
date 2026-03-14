"""Публичный API пакета `smsru_api`.

Экспортирует синхронный и асинхронный клиенты, а также алиасы для обратной
совместимости со старыми версиями библиотеки.
"""

from .client import Client as SmsRu
from .aioclient import AsyncClient as AsyncSmsRu
from .client import Client
from .aioclient import AsyncClient

__all__ = ["Client", "AsyncClient", "SmsRu", "AsyncSmsRu"]
