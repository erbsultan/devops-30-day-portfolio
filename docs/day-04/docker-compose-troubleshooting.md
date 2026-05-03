# Day 4 — Docker Compose Troubleshooting 🧯

## 🎯 Цель

Зафиксировать основные проблемы Day 4: timing issue при первом `curl`, Redis memory overcommit warning, случайный public bind `0.0.0.0` и проверку healthchecks.

## Ошибка 1 — `curl: Recv failure` сразу после старта

| Поле | Значение |
|---|---|
| Stage | First `curl` after `docker compose up -d --build` |
| Symptom | `curl: (56) Recv failure: Connection reset by peer` |
| Cause | API container был в состоянии `health: starting`; Flask server еще не был готов |
| Fix | Подождать 1-2 секунды, повторить `curl`, проверить `docker compose ps` и logs |

### Symptom

```bash
curl http://localhost:5000/
```

```text
curl: (56) Recv failure: Connection reset by peer
```

### Cause

`docker compose up -d` возвращает управление сразу после старта containers. В этот момент процесс Flask может еще стартовать, а healthcheck может показывать `starting`.

### ✅ Fix

```bash
docker compose ps
docker compose logs --tail=30 api
sleep 2
curl http://localhost:5000/healthz
```

Ожидаемый ответ:

```json
{"status":"ok"}
```

## Ошибка 2 — Redis memory overcommit warning

| Поле | Значение |
|---|---|
| Stage | Redis startup logs |
| Symptom | `WARNING Memory overcommit must be enabled!` |
| Cause | Linux kernel setting `vm.overcommit_memory` не включен |
| Fix | Добавить sysctl config и применить `sudo sysctl --system` |

### Symptom

```bash
docker compose logs --tail=30 redis
```

```text
WARNING Memory overcommit must be enabled!
```

### ✅ Fix

```bash
echo 'vm.overcommit_memory = 1' | sudo tee /etc/sysctl.d/99-redis-overcommit.conf
sudo sysctl --system
```

Перезапуск:

```bash
docker compose down
docker compose up -d
docker compose logs --tail=20 redis
```

Оставшийся warning:

```text
Warning: no config file specified
```

Это нормально для учебной lab: Redis использует default config.

## Ошибка 3 — Security issue: `0.0.0.0:5000->5000/tcp`

| Поле | Значение |
|---|---|
| Stage | `docker compose ps` |
| Symptom | `0.0.0.0:5000->5000/tcp` |
| Risk | API слушает на всех host interfaces |
| Fix | Bind host port к `127.0.0.1` |

### ❌ Небезопасно для lab

```yaml
ports:
  - "5000:5000"
```

Такой mapping может слушать на `0.0.0.0`, то есть на всех interfaces VM. Даже если Oracle Security List не открывает порт, лучше не публиковать сервис шире, чем нужно.

### ✅ Fix

```yaml
ports:
  - "127.0.0.1:5000:5000"
```

Проверка:

```bash
docker compose ps
```

Ожидаемо:

```text
127.0.0.1:5000->5000/tcp
```

## Проверка healthchecks

```bash
docker compose ps
```

Все сервисы должны быть `healthy`:

- `compose-api`;
- `compose-postgres`;
- `compose-redis`.

Проверить logs:

```bash
docker compose logs --tail=30 api
docker compose logs --tail=30 postgres
docker compose logs --tail=30 redis
```

Проверить endpoints:

```bash
curl http://localhost:5000/
curl http://localhost:5000/healthz
curl http://localhost:5000/redis
curl http://localhost:5000/db
```

## ✅ Troubleshooting checklist

- [x] Проверить `docker compose ps`.
- [x] Дождаться `healthy`, если app еще `starting`.
- [x] Смотреть logs конкретного service.
- [x] Проверять API только через `localhost`.
- [x] Убедиться, что port mapping показывает `127.0.0.1:5000->5000/tcp`.
- [x] Не открывать `5000`, `5432`, `6379` в Oracle Security List без необходимости.
