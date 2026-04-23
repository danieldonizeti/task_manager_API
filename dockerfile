FROM python:3.12-slim

#Evitando criação de arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1

#log em tempo real
ENV PYTHONUNBUFFERED 1

WORKDIR /app

#Dependencias do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#Copiando o requirements
COPY requirements.txt .

#Instalando as dependencias do python
RUN pip install --upgrade pip && pip install -r requirements.txt

#Copiando o projeto
COPY . .

#Expondo a porta
EXPOSE 8000

#Comando para rodar a aplicação
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
