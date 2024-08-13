
docker build -t meu-python-app .


docker run \
    --restart=always -dit \
    --name gtin \
    --network=minha_rede --ip 172.18.0.35 -p 3005:80 \
    -v /projeto/python/gtin/app/:/app \
    meu-python-app
