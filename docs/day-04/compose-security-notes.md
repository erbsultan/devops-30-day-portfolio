# Day 4 — Compose Security Notes 🔐

## 🎯 Цель

Зафиксировать security decisions для Docker Compose lab: localhost binding, закрытые DB/cache ports, `.env` hygiene, healthchecks и осознанное открытие public ports.

## Почему API bind на `127.0.0.1` безопаснее

Для учебной lab API проверялся только внутри Oracle VM:

```bash
curl http://localhost:5000/healthz
```

Поэтому host port не должен слушать на всех interfaces:

```yaml
ports:
  - "127.0.0.1:5000:5000"
```

Такой binding означает:

- API доступен на VM через `localhost`;
- API не слушает public interface напрямую;
- troubleshooting можно делать без изменения Oracle Security List;
- меньше шанс случайно показать учебный сервис в интернет.

## Почему Redis/PostgreSQL не публикуются наружу

PostgreSQL и Redis нужны только API service внутри Docker network.

Они не имеют `ports:` в `compose.yaml`, поэтому:

- PostgreSQL не публикует `5432` на host;
- Redis не публикует `6379` на host;
- внешние клиенты не могут подключиться напрямую через public interface;
- API остается единственной точкой доступа к данным.

## Почему `.env` не коммитить

`.env` может содержать реальные passwords, tokens, service URLs и другие secrets.

Правило:

```text
.env
```

должно быть в `.gitignore`, а также исключено из build context через `.dockerignore`.

## Почему `.env.example` можно коммитить

`.env.example` содержит только безопасный шаблон:

```env
POSTGRES_DB=appdb
POSTGRES_USER=appuser
POSTGRES_PASSWORD=apppassword
POSTGRES_HOST=postgres

REDIS_HOST=redis
REDIS_PORT=6379
```

Это помогает повторить lab без публикации реальных secrets.

## Почему healthchecks полезны

Healthchecks дают Compose понятное состояние сервисов:

- API отвечает на `/healthz`;
- PostgreSQL готов через `pg_isready`;
- Redis готов через `redis-cli ping`;
- `depends_on.condition: service_healthy` снижает race conditions при старте.

## Public ports открываем только осознанно

Перед публикацией port наружу нужно проверить:

- нужен ли public access вообще;
- есть ли authentication;
- открыт ли port в UFW;
- открыт ли port в Oracle Security List;
- нет ли secrets в response/logs;
- можно ли ограничить source CIDR, например `<HOME_PUBLIC_IP>/32`.

## ✅ Security checklist

- [x] API bound to `127.0.0.1`.
- [x] PostgreSQL port не опубликован.
- [x] Redis port не опубликован.
- [x] Oracle Security List не открывала `5000`, `5432`, `6379`.
- [x] UFW не открывал эти ports.
- [x] `.env` не коммитится.
- [x] `.env.example` безопасен как template.
- [x] Public IP заменяется на `<ORACLE_PUBLIC_IP>`.
