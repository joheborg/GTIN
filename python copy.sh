
docker build -t meu-python-app .


docker run \
    --restart=always -dit \
    --name flask-previsao \
    --network=minha_rede --ip 172.18.0.40 -p 3011:5000 \
    -v /projeto/python/previsaotempo/app/:/app \
    meu-python-app
