# Day 3 — Docker Basics on Oracle VM 🐳

## 🎯 Цель дня

Установить Docker Engine и Docker Compose plugin на Oracle VM, проверить базовую работу контейнеров и собрать простой Python demo app в Docker image.

Фокус Day 3:

- [x] установить Docker на Ubuntu `24.04.4 LTS`;
- [x] настроить запуск Docker без `sudo` через `docker` group;
- [x] проверить Docker Engine и Docker Compose plugin;
- [x] запустить test container с `nginx`;
- [x] собрать и запустить собственный Python container;
- [x] задокументировать ошибки, cleanup и security notes.

## 🧱 Контекст сервера

| Поле | Значение |
|---|---|
| Cloud | Oracle Cloud Infrastructure |
| Region | `<ORACLE_REGION>` |
| Hostname | `oci-k3s-master` |
| OS | Ubuntu `24.04.4 LTS` |
| Architecture | `arm64` |
| Shape | `VM.Standard.A2.Flex` |
| Role | Future `k3s` master node |
| VM source | Created on Day 2 |
| Public IP | `<ORACLE_PUBLIC_IP>` |
| Payment source | Oracle trial credits |
| Cloud ingress | SSH only from `<HOME_PUBLIC_IP>/32` |
| Host firewall | UFW active |

## ✅ Что было сделано

1. Подключились к Oracle VM `oci-k3s-master`.
2. Установили prerequisites для Docker apt repository.
3. Добавили официальный Docker GPG key и Docker apt source.
4. Установили Docker Engine, Docker CLI, `containerd`, Buildx plugin и Docker Compose plugin.
5. Добавили пользователя в `docker` group.
6. Проверили версии Docker и Compose.
7. Запустили `nginx` test container на локальном порту `8080`.
8. Собрали Python demo app image `day3-python-app:v1`.
9. Запустили container на локальном порту `5000`.
10. Проверили app через `curl http://localhost:5000`.
11. Остановили и удалили test containers.

## 🧰 Установка Docker Engine

### Install prerequisites

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
```

> Troubleshooting note: во время установки была опечатка `ca-cerftifcate`, из-за чего `apt` вернул `E: Unable to locate package ca-cerftifcate`. Правильный пакет: `ca-certificates`.

### Add Docker GPG key

```bash
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

### Add Docker apt repository

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Install Docker packages

```bash
sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Установленные компоненты:

| Component | Purpose |
|---|---|
| `docker-ce` | Docker Engine daemon |
| `docker-ce-cli` | Docker CLI |
| `containerd.io` | Container runtime |
| `docker-buildx-plugin` | Modern image build workflow |
| `docker-compose-plugin` | `docker compose` command |

## 👤 Docker post-install

Пользователь был добавлен в `docker` group:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

Важно: membership в `docker` group дает root-level privileges на хосте. Добавлять туда нужно только доверенных пользователей.

## 🔍 Проверка Docker

```bash
docker --version
docker compose version
sudo systemctl status docker --no-pager
docker ps
```

Ожидаемый результат:

- Docker CLI отвечает;
- Docker Compose plugin установлен;
- `docker.service` работает;
- `docker ps` выполняется без `sudo`.

## 🌐 Nginx test container

Для быстрой проверки был запущен `nginx` container:

```bash
docker run -d --name day3-nginx -p 8080:80 nginx:stable
curl http://localhost:8080
docker ps
```

После проверки container был остановлен и удален:

```bash
docker stop day3-nginx
docker rm day3-nginx
```

Security detail: порт `8080` не открывался в Oracle Security List. Проверка выполнялась только локально внутри VM через `localhost`.

## 🐍 Создание Python demo app

Рабочая директория на сервере:

```bash
~/day3-docker-demo
```

Dockerfile:

```Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

Python app:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        hostname = socket.gethostname()
        body = f"Hello from Docker on {hostname}\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())

server = HTTPServer(("0.0.0.0", 5000), Handler)
print("Server running on port 5000")
server.serve_forever()
```

## 🏗️ Сборка Docker image

Первая сборка упала, потому что `app.py` отсутствовал в build context:

```text
ERROR: failed to build: failed to solve: failed to compute cache key
"/app.py": not found
```

Причина: Dockerfile содержит `COPY app.py .`, но файла `app.py` рядом с Dockerfile еще не было.

После создания `app.py` image был собран:

```bash
docker build -t day3-python-app:v1 .
```

## ▶️ Запуск container

```bash
docker run -d --name day3-python-app -p 5000:5000 day3-python-app:v1
```

Первый `curl` сразу после запуска вернул:

```text
curl: (56) Recv failure: Connection reset by peer
```

Причина: container уже стартовал, но Python HTTP server еще не успел полностью подняться.

Повторный запрос сработал:

```bash
curl http://localhost:5000
```

Ответ:

```text
Hello from Docker on <container-id>
```

Дополнительные проверки:

```bash
docker ps
docker logs day3-python-app
docker images
```

## 🧹 Cleanup

После проверки containers были остановлены и удалены:

```bash
docker stop day3-python-app
docker rm day3-python-app
```

Image `day3-python-app:v1` можно оставить локально для обучения.

## 🔐 Security notes

- Порты `5000` и `8080` не открывались наружу.
- Проверки выполнялись только через `localhost` внутри Oracle VM.
- Oracle Security List должна по-прежнему открывать только SSH `TCP 22` с `<HOME_PUBLIC_IP>/32`.
- UFW остается активным как host-level firewall.
- `docker` group имеет root-level privileges.
- Не хранить secrets в Docker images.
- Использовать `.dockerignore`, чтобы не отправлять лишние файлы в build context.
- В публичной документации не фиксировать реальные public IP, OCID, email, billing, subscription или account details.

## ✅ Финальный checklist

- [x] Docker Engine установлен.
- [x] Docker Compose plugin установлен.
- [x] Пользователь добавлен в `docker` group.
- [x] `docker --version` проверен.
- [x] `docker compose version` проверен.
- [x] `docker ps` работает без `sudo`.
- [x] `nginx` test container запущен и удален.
- [x] Python demo app собран в image.
- [x] Python container запущен и проверен через `curl`.
- [x] Test containers остановлены и удалены.
- [x] Порты `5000` и `8080` не открывались наружу.
- [x] Troubleshooting notes задокументированы.

## 🧭 Next steps для Day 4

- [ ] Перейти от одиночного `docker run` к `docker compose`.
- [ ] Собрать multi-container app stack.
- [ ] Зафиксировать `compose.yaml`.
- [ ] Добавить health checks и restart policy.
- [ ] Продолжать держать внешние порты закрытыми, пока они не нужны для конкретной задачи.
