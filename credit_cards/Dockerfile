# -------------------------
# 1. Base stage: Builder
# -------------------------
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.1.4 \
    POETRY_HOME="/opt/poetry" \
    PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry install --without dev --no-root

COPY . .

RUN poetry install --without dev


# -------------------------
# 2. Runtime stage: Final image
# -------------------------
FROM python:3.12-slim AS runner

RUN useradd -m appuser

WORKDIR /app

COPY --from=builder /app /app
COPY --from=builder /usr/local /usr/local

USER appuser

EXPOSE 9000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "9000"]
