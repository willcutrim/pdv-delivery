# Use a imagem base do Python
FROM python:3.10

# Defina variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Defina o diretório de trabalho no container
WORKDIR /code

# Instale as dependências do sistema
RUN apt-get update && \
    apt-get install -y postgresql-client

# Instale as dependências Python
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt 

# Copie o código do aplicativo para o contêiner
COPY . /code/
