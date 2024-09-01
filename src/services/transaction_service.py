"""Transaction service module."""

from __future__ import annotations

from dataclasses import dataclass

from config import BASE_CURRENCY
from persistence.repo import TransactionRepository, repo_dependency
from schemas.transaction_schema import (
    EnrichedTransactionSchema,
    IncomingTransactionSchema,
)
from services.exchange_rates_service import (
    ExchangeRatesService,
    get_exchange_rates_service,
)


@dataclass(frozen=True, slots=True)
class ConversionData:
    """Conversion class.
    Holds the target currency, the conversion rate and the converted amount.
    """

    target_currency: str
    exchange_rate: float
    target_amount: float


class TransactionService:
    """Transaction service class."""

    def __init__(
        self,
        repo: TransactionRepository = repo_dependency(),
    ) -> None:
        """Initialize service."""
        self.repo = repo

    def _get_rate(
        self,
        currency: str,
        service: ExchangeRatesService = get_exchange_rates_service(),
    ) -> float:
        """Get exchange rate."""
        return service.get_rate(currency)

    def save_transaction(
        self,
        transaction_data: IncomingTransactionSchema,
    ) -> dict[str, str]:
        """Save transaction."""
        rate: float = self._get_rate(transaction_data.currency)

        conversion_data = ConversionData(
            target_currency=BASE_CURRENCY,
            exchange_rate=rate,
            target_amount=round(transaction_data.amount / rate, 2),
        )

        new_transaction = EnrichedTransactionSchema(
            transaction_id=transaction_data.transaction_id,
            user_id=transaction_data.user_id,
            original_amount=transaction_data.amount,
            original_currency=transaction_data.currency,
            converted_amount=conversion_data.target_amount,
            target_currency=conversion_data.target_currency,
            exchange_rate=conversion_data.exchange_rate,
            timestamp=transaction_data.timestamp,
        )

        self.repo.add_transaction(new_transaction)
        return {"status": "Transaction saved successfully"}


def transaction_service_dependency() -> TransactionService:
    """Get transaction service instance."""
    return TransactionService()
