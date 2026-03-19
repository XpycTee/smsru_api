# Документация `smsru_api`

Каталог `docs/` содержит локальную копию подробной документации проекта и
служит каноническим источником описания API внутри репозитория.

## Содержимое

- [Обзор API](api-overview.md)
- [Отправка сообщений](messages.md)
- [Авторизация по звонку](callcheck.md)
- [Баланс и лимиты](account.md)
- [Стоп-лист](stoplist.md)
- [Callbacks и webhooks](callbacks.md)
- [Синхронные и асинхронные примеры](sync-async.md)

## Как читать документацию

- Начните с [обзора API](api-overview.md), если хотите быстро понять состав
  публичных методов.
- Откройте [отправку сообщений](messages.md), если вас интересует `send()` или
  `cost()`.
- Используйте [примеры sync/async](sync-async.md), если нужно выбрать подход к
  интеграции в проект.

## Источники истины

- `README.md` — краткий старт и обзор возможностей.
- `docs/` — подробные инструкции и примеры.
- docstring'и в `smsru_api/*.py` — точечная справка по параметрам и
  ограничениям прямо в IDE.

## Тестовый контур

Для безопасной локальной проверки достаточно:

```sh
.venv/bin/python -m pip install -e ".[test]"
.venv/bin/python -m pytest
```

Эта команда запускает только unit-тесты. Для отдельной проверки совместимости с
`Python 3.14` используйте отдельное окружение:

```sh
python3.14 -m venv .venv314
.venv314/bin/python -m pip install -e ".[test]"
.venv314/bin/python -m pytest tests/test_smsru.py
```

Live-тесты нужно включать явно:

```sh
.venv/bin/python -m pytest tests/test_live.py -m live
```

Для live-режима нужны `SMSRU_API_ID` и `SMSRU_TEST_PHONE`. Если установлен
`python-dotenv`, значения могут быть прочитаны из `.env`, но только при
`SMSRU_LOAD_DOTENV=true`.
