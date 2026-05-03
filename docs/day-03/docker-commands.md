# Day 3 — Docker Commands 📋

## 🎯 Назначение

Полный список команд Day 3 в логическом порядке: установка Docker, post-install setup, test containers, Python demo app, проверки и cleanup.

## 1. Install prerequisites

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
```

## 2. Add Docker repo

```bash
sudo install -m 0755 -d /etc/apt/keyrings
```

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

```bash
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

```bash
sudo apt update
```

## 3. Install Docker

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 4. Post-install docker group

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## 5. Docker version checks

```bash
docker --version
docker compose version
sudo systemctl status docker --no-pager
docker ps
```

## 6. Nginx test container

```bash
docker run -d --name day3-nginx -p 8080:80 nginx:stable
curl http://localhost:8080
docker ps
```

Cleanup:

```bash
docker stop day3-nginx
docker rm day3-nginx
```

Note: порт `8080` проверялся только локально через `localhost` внутри VM.

## 7. Demo app files

Рабочая директория:

```bash
mkdir -p ~/day3-docker-demo
cd ~/day3-docker-demo
```

`Dockerfile`:

```Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

`app.py`:

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

Проверить build context:

```bash
ls -la
```

## 8. Docker build

```bash
docker build -t day3-python-app:v1 .
```

## 9. Docker run

```bash
docker run -d --name day3-python-app -p 5000:5000 day3-python-app:v1
```

## 10. Curl

```bash
curl http://localhost:5000
```

Ожидаемый ответ:

```text
Hello from Docker on <container-id>
```

Если первый запрос сразу после запуска container вернул connection reset, повторить через 1-2 секунды.

## 11. Logs and inspection

```bash
docker ps
docker logs day3-python-app
docker images
```

## 12. Cleanup

```bash
docker stop day3-python-app
docker rm day3-python-app
```

Image можно оставить для обучения:

```bash
docker images
```

## 🔐 Security reminders

- Не открывать `5000` и `8080` в Oracle Security List без необходимости.
- Для Day 3 достаточно локальных checks через `localhost`.
- Cloud ingress должен оставаться: `<HOME_PUBLIC_IP>/32 → TCP 22`.
- UFW должен оставаться active.
