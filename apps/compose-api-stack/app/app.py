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
