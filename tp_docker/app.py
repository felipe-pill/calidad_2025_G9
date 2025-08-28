import os
import time
import redis
from flask import Flask
from splitio import get_factory

app = Flask(__name__)

# ------------ Redis helpers ------------
def wait_for_redis():
    """Wait until Redis is available (same behavior as your current app)."""
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    client = redis.Redis(host=redis_host, port=redis_port, db=0)
    for _ in range(30):
        try:
            client.ping()
            return client
        except Exception:
            time.sleep(1)
    raise RuntimeError("Redis not available")

# ------------ Split initialization (minimal) ------------
SPLIT_API_KEY = os.getenv("SPLIT_SDK_API_KEY", "").strip()
SPLIT_FEATURE_NAME = os.getenv("SPLIT_FEATURE_NAME", "background_color").strip()
split_client = None

if SPLIT_API_KEY:
    try:
        split_factory = get_factory(SPLIT_API_KEY)
        split_client = split_factory.client()
        print("✅ Split client created")
    except Exception as e:
        print(f"⚠️ Split init warning: {e}")

# ------------ Routes ------------
@app.route('/')
def contador_visitas():
    try:
        redis_client = wait_for_redis()
        visitas = redis_client.incr('visitas')

        # Ask Split for treatment (probabilistic rollout)
        treatment = 'control'
        bg_style = ''
        try:
            if split_client:
                # Use a consistent key for Split treatment
                treatment = split_client.get_treatment(
                    key='default_key',  # Use a static or session-based key
                    feature_name=SPLIT_FEATURE_NAME
                )
                print(f"ℹ️ Split returned treatment={treatment}")
                if treatment == 'red':
                    bg_style = 'background-color: red;'
                elif treatment == 'green':
                    bg_style = 'background-color: green;'
        except Exception as e:
            print(f"⚠️ Split get_treatment warning: {e}")

        return f"""
        <html>
            <body style="font-family: Arial; text-align: center; padding: 50px; {bg_style}">
                <h1>📊 Contador de Visitas</h1>
                <p style="font-size: 24px;">¡Número de visitas: <strong>{visitas}</strong>! 🎉</p>
                <p>✅ Redis funcionando correctamente</p>
                <p><small>treatment = {treatment}</small></p>
                <a href="/reiniciar">🔄 Reiniciar contador</a> | 
                <a href="/health">❤️ Health check</a>
            </body>
        </html>
        """
    except Exception as e:
        return f"❌ Error: {e}"

@app.route('/reiniciar')
def reiniciar():
    try:
        redis_client = wait_for_redis()
        redis_client.set('visitas', 0)
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
