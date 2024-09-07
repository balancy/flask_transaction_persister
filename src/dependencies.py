"""App dependency injection factories module."""

from injector import Binder, Injector, singleton

from application.services.exchange_rates_service import ExchangeRatesService
from application.services.processing_services import (
    EnqueuedTransactionProcessingService,
    IncomingTransactionProcessingService,
)
from infrastructure.external_api.clients import ExternalExchangeRatesClient
from infrastructure.messaging.queue_client import QueueClient
from infrastructure.persistence.repositories import TransactionRepository


def configure_dependencies_for_web_app(binder: Binder) -> None:
    """Configure dependencies for Flask-Injector."""
    binder.bind(
        TransactionRepository,
        to=TransactionRepository,
        scope=singleton,
    )
    binder.bind(
        IncomingTransactionProcessingService,
        to=IncomingTransactionProcessingService,
        scope=singleton,
    )
    binder.bind(
        QueueClient,
        to=QueueClient,
        scope=singleton,
    )


def configure_dependencies_for_celery_app(binder: Binder) -> None:
    """Configure dependencies for celery."""
    binder.bind(
        TransactionRepository,
        to=TransactionRepository,
        scope=singleton,
    )
    binder.bind(
        ExchangeRatesService,
        to=ExchangeRatesService,
        scope=singleton,
    )
    binder.bind(
        EnqueuedTransactionProcessingService,
        to=EnqueuedTransactionProcessingService,
        scope=singleton,
    )
    binder.bind(
        ExternalExchangeRatesClient,
        to=ExternalExchangeRatesClient,
        scope=singleton,
    )


celery_injector = Injector([configure_dependencies_for_celery_app])
