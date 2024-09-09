"""Tests for transaction processing service logic."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from application.services.processing_services import (
    EnqueuedTransactionProcessingService,
    IncomingTransactionProcessingService,
)
from tests.stubs import NoOpLogger

from .stubs import CORRECT_INCOMING_TRANSACTION

if TYPE_CHECKING:
    from .stubs import (
        ExternalExchangeRatesClientStub,
        QueueClientStub,
        TransactionRepositoryStub,
    )


@pytest.fixture
def incoming_transaction_service(
    queue_client_stub: QueueClientStub,
    transaction_repository_stub: TransactionRepositoryStub,
) -> IncomingTransactionProcessingService:
    """Fixture for incoming transaction processing service."""
    return IncomingTransactionProcessingService(
        queue_client=queue_client_stub,
        repo=transaction_repository_stub,
        logger=NoOpLogger("test"),
    )


@pytest.fixture
def enqueued_transaction_service(
    external_exchange_rates_client_stub: ExternalExchangeRatesClientStub,
    transaction_repository_stub: TransactionRepositoryStub,
) -> EnqueuedTransactionProcessingService:
    """Fixture for enqueued transaction processing service."""
    return EnqueuedTransactionProcessingService(
        exchange_rates_client=external_exchange_rates_client_stub,
        repo=transaction_repository_stub,
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
