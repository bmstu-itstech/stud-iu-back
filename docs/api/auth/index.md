# Auth

## Секрет для подписи

Токены подписываются секретным ключом Django - переменной окружения `DJANGO_SECRET_KEY`.

> Ключ должен быть не короче 32 символов, иначе сервер отклонит токен.

## Получение токена

В Docker:

```shell
docker compose exec backend python -m libs.tokens --days 60
```

На сервере, если сервис запущен через `docker-compose.ci.yaml`:

```shell
docker exec stud-iu-backend python -m libs.tokens --days 60
```

> На сервере нет `.env`: `DJANGO_SECRET_KEY` передаётся контейнеру при деплое и есть только внутри него. Поэтому скрипт нужно запускать в контейнере, а не на самом сервере.

Локально:

```shell
uv run python -m libs.tokens --days 60
```
