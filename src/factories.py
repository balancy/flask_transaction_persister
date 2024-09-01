"""App dependency injection factories module."""

from injector import Binder, singleton

from persistence.repo import TransactionRepository
from services.exchange_rates_service import ExchangeRatesService
from services.transaction_service import TransactionService


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
