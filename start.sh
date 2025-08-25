#!/bin/bash

# Iniciar Redis en segundo plano
echo "🚀 Iniciando Redis server..."
redis-server --daemonize yes

# Esperar a que Redis esté listo
sleep 2

# Verificar Redis
if redis-cli ping | grep -q "PONG"; then
    echo "✅ Redis está funcionando"
else
    echo "❌ Redis no se pudo iniciar"
    exit 1
fi

# Iniciar Flask
echo "🚀 Iniciando aplicación Flask..."
exec python app.py