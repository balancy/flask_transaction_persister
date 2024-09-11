"""Module with fixtures for the application layer tests."""

import pytest

from .stubs import (
    ExternalExchangeRatesClientStub,
    QueueClientStub,
    TransactionRepositoryStub,
)


@pytest.fixture
def queue_client_stub() -> QueueClientStub:
    """Fixture that returns a QueueClientStub instance."""
    return QueueClientStub()


@pytest.fixture
def transaction_repository_stub() -> TransactionRepositoryStub:
    """Fixture that returns a TransactionRepositoryStub instance."""
    return TransactionRepositoryStub()


@pytest.fixture
def external_exchange_rates_client_stub() -> ExternalExchangeRatesClientStub:
    """Fixture that returns a ExternalExchangeRatesClientStub instance."""
    return ExternalExchangeRatesClientStub()
