"""Tests for transaction processing service logic."""

import pytest

from application.services.processing_services import (
    EnqueuedTransactionProcessingService,
    IncomingTransactionProcessingService,
)
from tests.stubs import NoOpLogger

from .stubs import (
    CORRECT_INCOMING_TRANSACTION,
    ExternalExchangeRatesClientStub,
    QueueClientStub,
    TransactionRepositoryStub,
)


@pytest.fixture()
def incoming_transaction_service() -> IncomingTransactionProcessingService:
    """Fixture for incoming transaction processing service."""
    queue_client_stub = QueueClientStub()
    transaction_repo_stub = TransactionRepositoryStub()
    return IncomingTransactionProcessingService(
        queue_client=queue_client_stub,
        repo=transaction_repo_stub,
        logger=NoOpLogger("test"),
    )


@pytest.fixture()
def enqueued_transaction_service() -> EnqueuedTransactionProcessingService:
    """Fixture for enqueued transaction processing service."""
    exchange_rates_client_stub = ExternalExchangeRatesClientStub()
    transaction_repo_stub = TransactionRepositoryStub()
    return EnqueuedTransactionProcessingService(
        exchange_rates_client=exchange_rates_client_stub,
        repo=transaction_repo_stub,
        logger=NoOpLogger("test"),
    )


def test_incoming_transaction_processing_service_correct_flow(
    incoming_transaction_service: IncomingTransactionProcessingService,
) -> None:
    """Test incoming transaction processing service correct flow."""
    incoming_transaction_service.process_transaction(
        CORRECT_INCOMING_TRANSACTION,
    )


def test_enqueued_transaction_processing_service_correct_flow(
    enqueued_transaction_service: EnqueuedTransactionProcessingService,
) -> None:
    """Test enqueued transaction processing service correct flow."""
    enqueued_transaction_service.process_transaction(
        CORRECT_INCOMING_TRANSACTION,
    )
