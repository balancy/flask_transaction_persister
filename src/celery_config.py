"""Celery configuration module."""

import logging

from celery import Celery

from config import IS_TRACING_ON, RABBITMQ_URL

logging.basicConfig(level=logging.DEBUG)

if IS_TRACING_ON:
    from utils.tracing import (
        init_instruments_for_celery_app,
        initialize_tracing,
    )

    initialize_tracing(service_name="celery + db")

celery_app = Celery("tasks", broker=RABBITMQ_URL, backend="rpc://")

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

if IS_TRACING_ON:
    init_instruments_for_celery_app()


from tasks import process_transaction  # noqa: E402, F401
