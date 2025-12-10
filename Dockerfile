FROM python:3.11-slim

# НОВЫЙ ШАГ: Создаем sources.list с HTTPS-ссылками, чтобы избежать проблем с ISP
RUN echo "deb https://deb.debian.org/debian trixie main" > /etc/apt/sources.list \
    && echo "deb https://deb.debian.org/debian trixie-updates main" >> /etc/apt/sources.list \
    && echo "deb https://deb.debian.org/debian-security trixie-security main" >> /etc/apt/sources.list

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl \
    && pip install --upgrade pip \
    && pip install "poetry==${POETRY_VERSION}" \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* README.md ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000"]