# Stage 1: builder stage
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
  curl \
  && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --only main

# Stage 2: Move dependencies without poetry for image to weight less
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . /app

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--reload"]