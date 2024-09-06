"""Module for processing services."""

from __future__ import annotations

from injector import inject

from application.services.exchange_rates_service import ExchangeRatesService
from config import TARGET_CURRENCY
from domain.models import IncomingTransaction, ProcessedTransaction
from infrastructure.messaging_queue_client import QueueClient
from infrastructure.persistence.repositories import TransactionRepository
from utils.app_logger import logger


class IncomingTransactionProcessingService:
    """Class for incoming transaction processing service."""

    @inject
    def __init__(
        self,
        queue_client: QueueClient,
        repo: TransactionRepository,
    ) -> None:
        """Initialize service."""
        self.queue_client = queue_client
        self.repo = repo

    def process_transaction(
        self,
        transaction_data: IncomingTransaction,
    ) -> dict[str, str]:
        """Process transaction."""
        logger.info(
            "Processing incoming transaction %s",
            transaction_data.transaction_id,
        )

        self.repo.save_incoming_transaction(transaction_data)
        logger.info(
            "Incoming transaction %s saved successfully",
            transaction_data.transaction_id,
        )

        self.queue_client.send_transaction_to_queue(
            transaction_data.to_dict(),
        )
        logger.info(
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
        repo: TransactionRepository,
        exchange_service: ExchangeRatesService,
    ) -> None:
        """Initialize service."""
        self.repo = repo
        self.exchange_service = exchange_service

    def process_transaction(
        self,
        transaction_data: IncomingTransaction,
    ) -> dict[str, str]:
        """Process transaction."""
        logger.info(
            "Processing dequeued transaction %s",
            transaction_data.transaction_id,
        )

        rate: float = self.exchange_service.get_rate(
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
        logger.info(message)

        return {"status": message}
