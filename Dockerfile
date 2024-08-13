# Use uma imagem base do Python
FROM python:3.11

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instale as bibliotecas Python necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão para iniciar a aplicação
CMD ["python", "API.py"]
