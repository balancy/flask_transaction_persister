"""Module for application protocols."""

from __future__ import annotations

from typing import Any, Protocol

from domain.models import IncomingTransaction, ProcessedTransaction


class ExchangeRatesClientProtocol(Protocol):
    """Protocol for exchange rate client, defining expected methods."""

    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Get the exchange rate between two currencies."""
        ...  # pragma: no cover


class QueueClientProtocol(Protocol):
    """Protocol for queue client, defining expected methods."""

    def send_transaction_to_queue(
        self,
        transaction_data: dict[str, Any],
    ) -> None:
        """Send transaction data to a queue."""
        ...  # pragma: no cover

    def close_connection(self) -> None:
        """Close the connection to the queue."""
        ...  # pragma: no cover


class TransactionRepositoryProtocol(Protocol):
    """Protocol for transaction repository, defining expected methods."""

    def save_incoming_transaction(
        self,
        transaction_data: IncomingTransaction,
    ) -> None:
        """Save incoming transaction data."""
        ...  # pragma: no cover

    def save_processed_transaction(
        self,
        transaction_data: ProcessedTransaction,
    ) -> None:
        """Save processed transaction data."""
        ...  # pragma: no cover
