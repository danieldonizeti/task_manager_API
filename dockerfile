FROM python:3.12-slim

# Evita criação de arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Log em tempo real
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiando e instalando dependências (cache de layers)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiando o projeto
COPY . .

# Coletando arquivos estáticos
RUN python manage.py collectstatic --noinput

# Usuário não-root (segurança)
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Expondo a porta
EXPOSE 8000

# Gunicorn para produção
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2", "--timeout", "120"]