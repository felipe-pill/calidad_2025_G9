docker build -t contador-visitas .

docker rm -f visitas redis 2>/dev/null || true
docker network create visitas-net 2>/dev/null || true

docker run -d --name redis --network visitas-net -p 6379:6379 redis:7-alpine

docker run -d \
  --name visitas \
  --network visitas-net \
  -p 5000:5000 \
  -e SPLIT_SDK_API_KEY='YOUR_SERVER_SDK_KEY' \
  -e SPLIT_FEATURE_NAME='background_color' \
  contador-visitas
