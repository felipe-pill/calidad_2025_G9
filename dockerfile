FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY app.py .
COPY start.sh .


RUN apt-get update && apt-get install -y \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x start.sh

EXPOSE 5000

CMD ["./start.sh"]