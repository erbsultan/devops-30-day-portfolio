# Day 3 Docker Demo App 🐍

## Что это

Простое Python HTTP demo app для Day 3. Приложение запускает HTTP server на порту `5000` и возвращает hostname container:

```text
Hello from Docker on <container-id>
```

Цель demo app — проверить базовый Docker workflow:

- [x] написать `Dockerfile`;
- [x] собрать image;
- [x] запустить container;
- [x] проверить app через `curl`;
- [x] остановить и удалить container.

## Файлы

| Файл | Назначение |
|---|---|
| `app.py` | Python HTTP server |
| `Dockerfile` | Инструкция сборки image |
| `.dockerignore` | Исключения из Docker build context |

## Собрать image

```bash
docker build -t day3-python-app:v1 .
```

## Запустить container

```bash
docker run -d --name day3-python-app -p 5000:5000 day3-python-app:v1
```

## Проверить через curl

```bash
curl http://localhost:5000
```

Ожидаемый ответ:

```text
Hello from Docker on <container-id>
```

Если первый `curl` сразу после запуска вернул connection reset, подождать 1-2 секунды и повторить запрос.

## Посмотреть logs

```bash
docker logs day3-python-app
```

## Остановить и удалить container

```bash
docker stop day3-python-app
docker rm day3-python-app
```

## Security note

На Day 3 порт `5000` проверялся только локально внутри Oracle VM через `localhost`.

Порт `5000` не открывался наружу в Oracle Security List. Cloud ingress должен оставаться ограниченным SSH-доступом:

```text
<HOME_PUBLIC_IP>/32 → TCP 22
```
