"""Messaging tasks module."""

from __future__ import annotations

from typing import Any

from celery import shared_task

from application.dtos import TransactionDTO
from application.services.modified_transaction_processing_services import (
    ModifiedTransactionProcessingService,
)
from infrastructure.messaging.di_container import di_injector
from utils.app_logger import logger
from utils.exceptions import TransactionIntegrityError


@shared_task
def process_transaction(
    transaction_data: dict[str, Any],
) -> Any:
    """Task delegating transaction processing to the application service."""
    transaction_dto = TransactionDTO.from_dict(transaction_data)
    transaction_service = di_injector.get(ModifiedTransactionProcessingService)

    try:
        result = transaction_service.process_transaction(transaction_dto)
    except TransactionIntegrityError as error:
        logger.error(str(error))
        return {"error": str(error)}

    return result
