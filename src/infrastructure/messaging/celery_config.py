"""Celery configuration module."""

from celery import Celery

celery_app = Celery(
    "tasks",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="rpc://",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

import infrastructure.messaging.tasks  # noqa: E402 F401
