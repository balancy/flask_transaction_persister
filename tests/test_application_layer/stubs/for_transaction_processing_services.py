"""Module with stubs for transaction processing services."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from domain.models import IncomingTransaction, ProcessedTransaction

CURRENCIES_PAIR = ("USD", "EUR")
RATE = 1.25

CORRECT_INCOMING_TRANSACTION = IncomingTransaction(
    transaction_id="123",
    user_id="456",
    amount=100,
    currency="USD",
    timestamp=datetime(2022, 1, 1),  # noqa: DTZ001
)


class QueueClientStub:
    """A stub implementation of the QueueClientProtocol."""

    def send_transaction_to_queue(
        self,
        transaction_data: dict[str, Any],
    ) -> None:
        """Stub implementation of send_transaction_to_queue."""
        assert transaction_data == CORRECT_INCOMING_TRANSACTION.to_dict()


class TransactionRepositoryStub:
    """A stub implementation of the TransactionRepositoryProtocol."""

    def save_incoming_transaction(
        self,
        transaction_data: IncomingTransaction,
    ) -> None:
        """Stub implementation of save_incoming_transaction."""
        assert transaction_data == CORRECT_INCOMING_TRANSACTION

    def save_processed_transaction(
        self,
        transaction_data: ProcessedTransaction,
    ) -> None:
        """Stub implementation of save_processed_transaction."""
        _, target_currency = CURRENCIES_PAIR
        correct_processed_transaction = ProcessedTransaction(
            transaction_id=CORRECT_INCOMING_TRANSACTION.transaction_id,
            user_id=CORRECT_INCOMING_TRANSACTION.user_id,
            original_amount=CORRECT_INCOMING_TRANSACTION.amount,
            original_currency=CORRECT_INCOMING_TRANSACTION.currency,
            timestamp=CORRECT_INCOMING_TRANSACTION.timestamp,
            converted_amount=CORRECT_INCOMING_TRANSACTION.amount / RATE,
            target_currency=target_currency,
            exchange_rate=RATE,
        )
        assert transaction_data == correct_processed_transaction


class ExchangeRatesServiceStub:
    """A stub implementation of the ExchangeRatesServiceProtocol."""

    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Stub implementation of get_rate."""
        assert (from_currency, to_currency) == CURRENCIES_PAIR
        return RATE
