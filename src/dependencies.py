"""App dependency injection factories module."""

from injector import Binder, singleton

from application.services.exchange_rates_service import ExchangeRatesService
from application.services.processing_services import (
    EnqueuedTransactionProcessingService,
)
from infrastructure.external_api.clients import ExternalExchangeRatesClient
from infrastructure.messaging.queue_client import QueueClient
from infrastructure.persistence.repositories import TransactionRepository
from src.application.services.processing_services import (
    IncomingTransactionProcessingService,
)


def configure_dependencies_for_app(binder: Binder) -> None:
    """Configure dependencies for Flask-Injector."""
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
        IncomingTransactionProcessingService,
        to=IncomingTransactionProcessingService,
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
    binder.bind(
        QueueClient,
        to=QueueClient,
        scope=singleton,
    )
