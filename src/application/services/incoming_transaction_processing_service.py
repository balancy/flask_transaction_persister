"""Module for asynchronous tasks service."""

from __future__ import annotations

from injector import inject

from application.dtos import TransactionDTO
from infrastructure.messaging.queue_client import QueueClient
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

    def _enqueue_transaction(self, transaction_data: TransactionDTO) -> None:
        """Process incoming transaction asynchronously."""
        self.queue_client.send_transaction_to_queue(transaction_data.to_dict())

    def process_transaction(
        self,
        transaction_data: TransactionDTO,
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

        self._enqueue_transaction(transaction_data)
        logger.info(
            "Transaction with rates calculation enqueued: %s",
            transaction_data.transaction_id,
        )

        return {
            "status": (
                f"Incoming transaction {transaction_data.transaction_id} "
                "saved and enqueued successfully"
            ),
        }
