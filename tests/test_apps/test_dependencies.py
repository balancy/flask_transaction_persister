"""Tests for the dependency injection configuration."""

import logging

import pytest
from injector import Injector

from application.protocols import (
    ExchangeRatesClientProtocol,
    QueueClientProtocol,
    TransactionRepositoryProtocol,
)
from application.services.processing_services import (
    EnqueuedTransactionProcessingService,
    IncomingTransactionProcessingService,
)
from dependencies import (
    configure_dependencies_for_celery_app,
    configure_dependencies_for_web_app,
)
from domain.protocols import ProcessingServiceProtocol
from infrastructure.external_api.clients import ExternalExchangeRatesClient
from infrastructure.messaging.queue_client import QueueClient
from infrastructure.persistence.repositories import TransactionRepository
from utils.app_logger import logger as app_logger


@pytest.fixture
def injector() -> Injector:
    """Fixture to create an Injector instance for testing."""
    return Injector()


def test_configure_dependencies_for_web_app(injector: Injector) -> None:
    """Test the web app dependency configuration."""
    injector.binder.install(configure_dependencies_for_web_app)

    assert isinstance(
        injector.get(TransactionRepositoryProtocol),
        TransactionRepository,
    )

    assert isinstance(
        injector.get(ProcessingServiceProtocol),
        IncomingTransactionProcessingService,
    )

    assert isinstance(injector.get(QueueClientProtocol), QueueClient)

    assert injector.get(logging.Logger) == app_logger


def test_configure_dependencies_for_celery_app(injector: Injector) -> None:
    """Test the Celery app dependency configuration."""
    injector.binder.install(configure_dependencies_for_celery_app)

    assert isinstance(
        injector.get(TransactionRepositoryProtocol),
        TransactionRepository,
    )

    assert isinstance(
        injector.get(ProcessingServiceProtocol),
        EnqueuedTransactionProcessingService,
    )

    assert isinstance(
        injector.get(ExchangeRatesClientProtocol),
        ExternalExchangeRatesClient,
    )

    assert injector.get(logging.Logger) == app_logger


def test_missing_binding(injector: Injector) -> None:
    """Test for unsatisfied requirements when bindings are missing."""
    assert injector.get(object) is None
