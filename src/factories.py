"""App dependency injection factories module."""

from injector import Binder, singleton

from application.services.exchange_rates_service import ExchangeRatesService
from application.services.transaction_service import TransactionService
from infrastructure.external_api.clients import ExternalExchangeRatesClient
from infrastructure.persistence.repositories import TransactionRepository


def configure_dependencies(binder: Binder) -> None:
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
        TransactionService,
        to=TransactionService,
        scope=singleton,
    )
    binder.bind(
        ExternalExchangeRatesClient,
        to=ExternalExchangeRatesClient,
        scope=singleton,
    )
