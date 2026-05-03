# Day 4 — Docker Compose Commands 📋

## 🎯 Назначение

Полный список команд Day 4: локальная структура проекта, файлы приложения, передача на Oracle VM, запуск Docker Compose stack, проверки, logs, Redis warning fix и cleanup.

## 1. Локальная структура проекта на Mac

```bash
cd ~/devops-portfolio
mkdir -p apps/compose-api-stack/app
cd apps/compose-api-stack
touch .dockerignore .env.example Dockerfile compose.yaml app/app.py app/requirements.txt
```

Проверка структуры:

```bash
find . -maxdepth 3 -type f | sort
```

## 2. Создание `app/app.py`

```bash
cat > app/app.py <<'EOF'
import os
import redis
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        database=os.getenv("POSTGRES_DB", "appdb"),
        user=os.getenv("POSTGRES_USER", "appuser"),
        password=os.getenv("POSTGRES_PASSWORD", "apppassword"),
    )

@app.get("/")
def index():
    return jsonify({
        "message": "Hello from Docker Compose API stack",
        "services": ["api", "postgres", "redis"]
    })

@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})

@app.get("/redis")
def redis_check():
    redis_client.incr("hits")
    return jsonify({"redis_hits": redis_client.get("hits")})

@app.get("/db")
def db_check():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({"postgres_version": version})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
EOF
```

## 3. Создание `app/requirements.txt`

```bash
cat > app/requirements.txt <<'EOF'
flask==3.0.3
redis==5.0.8
psycopg2-binary==2.9.9
EOF
```

## 4. Создание `Dockerfile`

```bash
cat > Dockerfile <<'EOF'
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py .

EXPOSE 5000

CMD ["python", "app.py"]
EOF
```

## 5. Создание `.dockerignore`

```bash
cat > .dockerignore <<'EOF'
__pycache__/
*.pyc
.env
.git
.DS_Store
EOF
```

## 6. Создание `.env.example`

```bash
cat > .env.example <<'EOF'
POSTGRES_DB=appdb
POSTGRES_USER=appuser
POSTGRES_PASSWORD=apppassword
POSTGRES_HOST=postgres

REDIS_HOST=redis
REDIS_PORT=6379
EOF
```

`.env` не коммитится. `.env.example` можно коммитить как template.

## 7. Создание `compose.yaml`

```bash
cat > compose.yaml <<'EOF'
services:
  api:
    build: .
    container_name: compose-api
    ports:
      - "127.0.0.1:5000:5000"
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: apppassword
      POSTGRES_HOST: postgres
      REDIS_HOST: redis
      REDIS_PORT: 6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/healthz')"]
      interval: 10s
      timeout: 3s
      retries: 5

  postgres:
    image: postgres:16-alpine
    container_name: compose-postgres
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: apppassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: compose-redis
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

volumes:
  postgres_data:
EOF
```

Security check:

```bash
grep '127.0.0.1:5000:5000' compose.yaml
```

## 8. Передача проекта на Oracle VM

```bash
rsync -avz -e "ssh -i ~/.ssh/devops_cloud_lab" \
  ~/devops-portfolio/apps/compose-api-stack/ \
  ubuntu@<ORACLE_PUBLIC_IP>:~/compose-api-stack/
```

## 9. Запуск stack на сервере

```bash
ssh -i ~/.ssh/devops_cloud_lab ubuntu@<ORACLE_PUBLIC_IP>
```

```bash
cd ~/compose-api-stack
docker compose up -d --build
docker compose ps
```

## 10. Curl checks

```bash
curl http://localhost:5000/
curl http://localhost:5000/healthz
curl http://localhost:5000/redis
curl http://localhost:5000/redis
curl http://localhost:5000/db
```

Ожидаемые ответы:

```json
{"message":"Hello from Docker Compose API stack","services":["api","postgres","redis"]}
```

```json
{"status":"ok"}
```

```json
{"redis_hits":"1"}
```

```json
{"redis_hits":"2"}
```

```json
{"postgres_version":"PostgreSQL 16.13 on aarch64-unknown-linux-musl, compiled by gcc (Alpine 15.2.0) 15.2.0, 64-bit"}
```

## 11. Logs

```bash
docker compose logs --tail=30 api
docker compose logs --tail=30 postgres
docker compose logs --tail=30 redis
```

## 12. Redis memory overcommit fix

```bash
echo 'vm.overcommit_memory = 1' | sudo tee /etc/sysctl.d/99-redis-overcommit.conf
sudo sysctl --system
```

Перезапуск stack:

```bash
cd ~/compose-api-stack
docker compose down
docker compose up -d
docker compose logs --tail=20 redis
```

Обычный Redis warning можно оставить для учебной lab:

```text
Warning: no config file specified
```

## 13. Cleanup

Остановить stack:

```bash
docker compose down
```

Остановить stack и удалить PostgreSQL volume:

```bash
docker compose down -v
```
