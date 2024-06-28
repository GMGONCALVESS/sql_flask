FROM python:3.7-alpine

WORKDIR /app

# Adiciona os arquivos da aplicação ao diretório de trabalho
ADD . /app

# Atualiza o gerenciador de pacotes e instala as dependências necessárias
RUN apk update && \
    apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    mariadb-dev

# Atualiza o pip para a versão mais recente
RUN pip3 install --upgrade pip

# Instala as dependências da aplicação
RUN pip3 install Flask mysql-connector-python

EXPOSE 8081

# Define o comando para iniciar a aplicação
CMD ["python3", "web_01_v2.py"]

