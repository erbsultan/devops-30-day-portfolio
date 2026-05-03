# Day 3 — Docker Troubleshooting 🧯

## 🎯 Цель

Зафиксировать ошибки Day 3, их симптомы, причины и правильные fixes. Это поможет быстрее диагностировать похожие проблемы при работе с Docker на Oracle VM.

## Ошибка 1 — typo в имени package

| Поле | Значение |
|---|---|
| Command | `sudo apt install -y ca-cerftifcate curl gnupg` |
| Symptom | `E: Unable to locate package ca-cerftifcate` |
| Root cause | Опечатка в имени пакета |
| Correct package | `ca-certificates` |

### ❌ Неправильно

```bash
sudo apt install -y ca-cerftifcate curl gnupg
```

### ✅ Fix

```bash
sudo apt install -y ca-certificates curl gnupg
```

### Что запомнить

`apt` ищет package name буквально. Если в имени пакета typo, Ubuntu не сможет найти пакет даже при рабочем apt repository.

## Ошибка 2 — Docker build failed: `app.py` not found

| Поле | Значение |
|---|---|
| Stage | `docker build` |
| Symptom | `"/app.py": not found` |
| Root cause | `app.py` отсутствовал в Docker build context |
| Fix | Создать `app.py` рядом с Dockerfile |

### Symptom

```text
ERROR: failed to build: failed to solve: failed to compute cache key
"/app.py": not found
```

### Root cause

Dockerfile содержал инструкцию:

```Dockerfile
COPY app.py .
```

Но файла `app.py` не было в текущей директории, из которой запускался build.

Docker build context — это директория, переданная в конце команды:

```bash
docker build -t day3-python-app:v1 .
```

В этом случае build context — текущая директория `.`.

### ✅ Fix

Проверить файлы:

```bash
ls -la
```

Убедиться, что рядом находятся:

```text
Dockerfile
app.py
```

Затем повторить build:

```bash
docker build -t day3-python-app:v1 .
```

## Ошибка 3 — `curl: Recv failure: Connection reset by peer`

| Поле | Значение |
|---|---|
| Stage | First `curl` after container start |
| Symptom | `curl: (56) Recv failure: Connection reset by peer` |
| Root cause | App еще не успел полностью подняться |
| Fix | Подождать 1-2 секунды и повторить `curl` |

### Symptom

```bash
curl http://localhost:5000
```

```text
curl: (56) Recv failure: Connection reset by peer
```

### Root cause

Container уже был создан и запущен, но Python HTTP server внутри container еще не был готов принять соединение.

Это timing issue, а не проблема Oracle Security List, потому что проверка выполнялась локально через `localhost`.

### ✅ Fix

Повторить запрос через 1-2 секунды:

```bash
curl http://localhost:5000
```

Проверить состояние container:

```bash
docker ps
docker logs day3-python-app
```

Ожидаемый успешный ответ:

```text
Hello from Docker on <container-id>
```

## ✅ Troubleshooting checklist

- [x] Проверять package names перед `apt install`.
- [x] Проверять build context через `ls -la`.
- [x] Держать `Dockerfile` и copied files в одной директории, если используется `COPY app.py .`.
- [x] После `docker run -d` учитывать, что app может стартовать не мгновенно.
- [x] Для диагностики использовать `docker ps`, `docker logs`, `docker images`.
- [x] Не открывать cloud ports для локального troubleshooting без необходимости.
