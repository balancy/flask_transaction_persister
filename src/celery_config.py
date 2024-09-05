"""Celery configuration module."""

from celery import Celery

from config import IS_METRICS_MONITORING_ON, IS_TRACING_ON, RABBITMQ_URL

if IS_TRACING_ON:
    from utils.tracing import initialize_tracing_for_celery_app

    initialize_tracing_for_celery_app(service_name="celery")

celery_app = Celery("tasks", broker=RABBITMQ_URL, backend="rpc://")

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)


from tasks import process_transaction  # noqa: E402, F401

if IS_METRICS_MONITORING_ON:
    from celery_prometheus import add_prometheus_option

    add_prometheus_option(celery_app)
