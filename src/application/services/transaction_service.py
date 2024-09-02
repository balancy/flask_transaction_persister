"""Transaction service module."""

from __future__ import annotations

from injector import inject

from application.dtos import TransactionDTO
from application.services.exchange_rates_service import ExchangeRatesService
from config import TARGET_CURRENCY
from domain.models import Transaction
from infrastructure.persistence.repositories import TransactionRepository


class TransactionService:
    """Transaction service class."""

    @inject
    def __init__(
        self,
        repo: TransactionRepository,
        exchange_service: ExchangeRatesService,
    ) -> None:
        """Initialize service."""
        self.repo = repo
        self.exchange_service = exchange_service

    def save_transaction(
        self,
        transaction_data: TransactionDTO,
    ) -> dict[str, str]:
        """Save transaction."""
        rate: float = self.exchange_service.get_rate(transaction_data.currency)

        transaction_to_save = Transaction(
            transaction_id=transaction_data.transaction_id,
            user_id=transaction_data.user_id,
            original_amount=transaction_data.amount,
            original_currency=transaction_data.currency,
            converted_amount=round(transaction_data.amount / rate, 2),
            target_currency=TARGET_CURRENCY,
            exchange_rate=rate,
            timestamp=transaction_data.timestamp,
        )

        self.repo.save(transaction_to_save)

        transaction_id = transaction_data.transaction_id

        return {"status": f"Transaction {transaction_id} saved successfully"}
