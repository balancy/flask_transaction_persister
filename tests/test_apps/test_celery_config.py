"""Tests for the Celery app configuration."""

from celery.app.task import Task

from celery_config import celery_app
from config import RABBITMQ_URL


def test_celery_app_basic_configuration() -> None:
    """Test the basic configuration of the Celery app."""
    assert celery_app.conf.task_serializer == "json"
    assert celery_app.conf.accept_content == ["json"]
    assert celery_app.conf.result_serializer == "json"
    assert celery_app.conf.timezone == "UTC"
    assert celery_app.conf.enable_utc is True
    assert celery_app.conf.broker_connection_retry_on_startup is True


def test_celery_app_broker_configuration() -> None:
    """Test the broker configuration of the Celery app."""
    assert celery_app.conf.broker_url == RABBITMQ_URL


def test_celery_app_imported_tasks() -> None:
    """Test correct tasks registration in celery app."""
    assert "tasks.process_transaction" in celery_app.tasks

    task = celery_app.tasks["tasks.process_transaction"]
    assert isinstance(task, Task)
