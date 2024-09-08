"""App dependency injection factories module."""

import logging

from injector import Binder, Injector, singleton

from application.protocols import (
    ExchangeRatesClientProtocol,
    QueueClientProtocol,
    TransactionRepositoryProtocol,
)
from application.services.exchange_rates_service import ExchangeRatesService
from application.services.processing_services import (
    EnqueuedTransactionProcessingService,
    IncomingTransactionProcessingService,
)
from domain.protocols import (
    ExchangeRatesServiceProtocol,
    ProcessingServiceProtocol,
)
from infrastructure.external_api.clients import ExternalExchangeRatesClient
from infrastructure.messaging.queue_client import QueueClient
from infrastructure.persistence.repositories import TransactionRepository
from utils.app_logger import logger as app_logger


def configure_dependencies_for_web_app(binder: Binder) -> None:
    """Configure dependencies for Flask-Injector."""
    binder.bind(
        TransactionRepositoryProtocol,
        to=TransactionRepository,
        scope=singleton,
    )
    binder.bind(
        ProcessingServiceProtocol,
        to=IncomingTransactionProcessingService,
        scope=singleton,
    )
    binder.bind(
        QueueClientProtocol,
        to=QueueClient,
        scope=singleton,
    )
    binder.bind(
        logging.Logger,
        to=app_logger,
        scope=singleton,
    )


def configure_dependencies_for_celery_app(binder: Binder) -> None:
    """Configure dependencies for celery."""
    binder.bind(
        TransactionRepositoryProtocol,
        to=TransactionRepository,
        scope=singleton,
    )
    binder.bind(
        ExchangeRatesServiceProtocol,
        to=ExchangeRatesService,
        scope=singleton,
    )
    binder.bind(
        ProcessingServiceProtocol,
        to=EnqueuedTransactionProcessingService,
        scope=singleton,
    )
    binder.bind(
        ExchangeRatesClientProtocol,
        to=ExternalExchangeRatesClient,
        scope=singleton,
    )
    binder.bind(
        logging.Logger,
        to=app_logger,
        scope=singleton,
    )


celery_injector = Injector([configure_dependencies_for_celery_app])
