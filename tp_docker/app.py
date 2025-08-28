import os
import time
import redis
from flask import Flask
from splitio import get_factory

app = Flask(__name__)

# -------- Redis --------
def wait_for_redis():
    host = os.getenv('REDIS_HOST', 'redis')
    port = int(os.getenv('REDIS_PORT', '6379'))
    client = redis.Redis(host=host, port=port, db=0)
    for _ in range(30):
        try:
            client.ping()
            return client
        except Exception:
            time.sleep(1)
    raise RuntimeError("Redis not available")

# -------- Split --------
SPLIT_API_KEY = os.getenv("SPLIT_SDK_API_KEY", "").strip()
SPLIT_FEATURE_NAME = os.getenv("SPLIT_FEATURE_NAME", "background_color").strip()
split_client = None

if SPLIT_API_KEY:
    factory = get_factory(SPLIT_API_KEY)
    try:
        factory.block_until_ready(10)  # wait for definitions to avoid 'control'
    except Exception:
        pass
    split_client = factory.client()

# -------- Routes --------
@app.route('/')
def contador_visitas():
    try:
        r = wait_for_redis()
        visitas = r.incr('visitas')

        # Per-visit rollout: each visit is a new evaluation key
        bg_style = ''
        if split_client:
            treatment = split_client.get_treatment(str(visitas), SPLIT_FEATURE_NAME)
            if treatment == 'red':
                bg_style = 'background-color: red;'
            elif treatment == 'green':
                bg_style = 'background-color: green;'
            # if 'control', stays white

        return f"""
        <html>
            <body style="min-height:100vh; margin:0; font-family: Arial; text-align: center; padding: 48px; {bg_style}">
                <h1>📊 Contador de Visitas</h1>
                <p style="font-size: 22px;">¡Número de visitas: <strong>{visitas}</strong>! 🎉</p>
                <p>✅ Redis OK</p>
                <a href="/reiniciar">🔄 Reiniciar contador</a> |
                <a href="/health">❤️ Health</a>
            </body>
        </html>
        """
    except Exception as e:
        return f"❌ Error: {e}"

@app.route('/reiniciar')
def reiniciar():
    try:
        r = wait_for_redis()
        r.set('visitas', 0)
        return "🔄 Contador reiniciado a 0."
    except Exception as e:
        return f"❌ Error: {e}"

@app.route('/health')
def health():
    try:
        wait_for_redis()
        return "OK"
    except Exception:
        return "NOT_OK", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
