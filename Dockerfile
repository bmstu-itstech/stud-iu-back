FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.1.4
RUN curl -sSL https://install.python-poetry.org | python3 -


ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false


WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main


FROM python:3.12-slim AS runtime

RUN addgroup --system app && adduser --system --ingroup app app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local

WORKDIR /app    
COPY . .

RUN chown -R app:app /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=stud_iu_back.settings

USER app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "stud_iu_back.wsgi:application"]
