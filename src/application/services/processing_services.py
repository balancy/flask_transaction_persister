"""Module for processing services."""

from __future__ import annotations

import logging  # noqa: TCH003

from injector import inject

from application.protocols import (
    ExchangeRatesClientProtocol,
    QueueClientProtocol,
    TransactionRepositoryProtocol,
)
from config import TARGET_CURRENCY
from domain.models import IncomingTransaction, ProcessedTransaction


class IncomingTransactionProcessingService:
    """Class for incoming transaction processing service."""

    @inject
    def __init__(
        self,
        queue_client: QueueClientProtocol,
        repo: TransactionRepositoryProtocol,
        logger: logging.Logger,
    ) -> None:
        """Initialize service."""
        self.queue_client = queue_client
        self.repo = repo
        self.logger = logger

    def process_transaction(
        self,
        transaction_data: IncomingTransaction,
    ) -> dict[str, str]:
        """Process transaction."""
        self.logger.info(
            "Processing incoming transaction %s",
            transaction_data.transaction_id,
        )

        self.repo.save_incoming_transaction(transaction_data)
        self.logger.info(
            "Incoming transaction %s saved successfully",
            transaction_data.transaction_id,
        )

        self.queue_client.send_transaction_to_queue(
            transaction_data.to_dict(),
        )
        self.logger.info(
            "Incoming transaction %s enqueued successfully",
            transaction_data.transaction_id,
        )

        return {
            "status": (
                f"Incoming transaction {transaction_data.transaction_id} "
                "saved and enqueued successfully"
            ),
        }


class EnqueuedTransactionProcessingService:
    """Class for enqueued transaction processing service."""

    @inject
    def __init__(
        self,
        repo: TransactionRepositoryProtocol,
        exchange_rates_client: ExchangeRatesClientProtocol,
        logger: logging.Logger,
    ) -> None:
        """Initialize service."""
        self.repo = repo
        self.exchange_rates_client = exchange_rates_client
        self.logger = logger

    def process_transaction(
        self,
        transaction_data: IncomingTransaction,
    ) -> dict[str, str]:
        """Process transaction."""
        self.logger.info(
            "Processing dequeued transaction %s",
            transaction_data.transaction_id,
        )

        rate: float = self.exchange_rates_client.get_rate(
            from_currency=transaction_data.currency,
            to_currency=TARGET_CURRENCY,
        )

        converted_amount: float = round(transaction_data.amount / rate, 2)

        transaction_to_save = ProcessedTransaction(
            transaction_id=transaction_data.transaction_id,
            user_id=transaction_data.user_id,
            original_amount=transaction_data.amount,
            original_currency=transaction_data.currency,
            converted_amount=converted_amount,
            target_currency=TARGET_CURRENCY,
            exchange_rate=rate,
            timestamp=transaction_data.timestamp,
        )

        self.repo.save_processed_transaction(transaction_to_save)

        transaction_id = transaction_data.transaction_id
        message = f"Transaction {transaction_id} saved successfully"
        self.logger.info(message)

        return {"status": message}
