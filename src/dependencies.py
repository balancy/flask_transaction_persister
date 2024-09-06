"""App dependency injection factories module."""

from flask import Flask
from injector import Binder, inject, singleton

from application.services.exchange_rates_service import ExchangeRatesService
from application.services.processing_services import (
    EnqueuedTransactionProcessingService,
    IncomingTransactionProcessingService,
)
from infrastructure.external_api_client import ExternalExchangeRatesClient
from infrastructure.messaging_queue_client import QueueClient
from infrastructure.persistence.repositories import TransactionRepository
from infrastructure.persistence.setup import init_db


def configure_persistence_dependencies_for_app(binder: Binder) -> None:
    """Configure persistence dependencies for Flask-Injector."""

    @singleton
    @inject
    def configure_db(app: Flask) -> None:
        """Initialize the database with the app."""
        init_db(app)  # Initialize the database through the dependency setup

    binder.bind(Flask, to=configure_db, scope=singleton)


def configure_extra_dependencies_for_app(binder: Binder) -> None:
    """Configure layered architecture dependencies for Flask-Injector."""

    binder.bind(
        TransactionRepository,
        to=TransactionRepository,
        scope=singleton,
    )
    binder.bind(ExchangeRatesService, to=ExchangeRatesService, scope=singleton)
    binder.bind(QueueClient, to=QueueClient, scope=singleton)
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
