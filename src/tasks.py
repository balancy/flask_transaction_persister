"""Messaging tasks module."""

from __future__ import annotations

from celery import shared_task
from pydantic import ValidationError

from application.schemas import IncomingTransactionSchema
from dependencies import celery_injector
from domain.models import IncomingTransaction
from domain.protocols import ProcessingServiceProtocol
from utils.app_logger import logger
from utils.context_managers import conditional_trace_context
from utils.exceptions import TransactionIntegrityError


@shared_task(bind=True, queue="transaction-queue")
def process_transaction(
    self,  # noqa: ARG001 ANN001
    transaction_data: dict,
) -> dict[str, str]:
    """Task that processes the transaction data retrieved from queue."""
    logger.info(
        "Processing transaction: %s",
        transaction_data["transaction_id"],
    )

    try:
        with conditional_trace_context(__name__, "validate_transaction"):
            IncomingTransactionSchema.model_validate(transaction_data)
    except ValidationError as error:
        logger.error("Validation error: %s", error.errors())
        raise

    transaction = IncomingTransaction.from_dict(transaction_data)
    transaction_service = celery_injector.get(ProcessingServiceProtocol)

    try:
        with conditional_trace_context(__name__, "process_transaction"):
            transaction_service.process_transaction(transaction)

    except TransactionIntegrityError as ex:
        logger.error(str(ex))
        return {"error": str(ex)}

    message = f"Processed transaction: {transaction.transaction_id}"
    logger.info(message)
    return {"status": message}
