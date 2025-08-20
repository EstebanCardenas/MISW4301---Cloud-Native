FROM python:3.12-slim

ENV POETRY_VERSION=2.1.4 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get install -y curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

COPY . .

EXPOSE 9000

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "9000"]
