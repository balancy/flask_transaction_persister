"""Module for domain protocols."""

from __future__ import annotations

from typing import Protocol

from domain.models import IncomingTransaction


class ProcessingServiceProtocol(Protocol):
    """Protocol for processing service, defining expected methods."""

    def process_transaction(
        self,
        transaction_data: IncomingTransaction,
    ) -> dict[str, str]:
        """Process transaction."""
        ...


class ExchangeRatesServiceProtocol(Protocol):
    """Protocol for exchange rates service, defining expected methods."""

    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Get the exchange rate between two currencies."""
        ...
