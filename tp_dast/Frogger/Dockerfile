FROM python:3.9-slim
WORKDIR /app

# SDL/X11 runtime libs often needed by pygame wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    libasound2 libx11-6 libxext6 libxrender1 libxrandr2 libxi6 \
    libxcursor1 libxfixes3 libglib2.0-0 libglu1-mesa \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends libpulse0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "FROGGER_RUN.py"]
