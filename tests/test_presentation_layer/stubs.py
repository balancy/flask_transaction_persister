"""Stubs for the presentation layer."""

from __future__ import annotations

from pydantic import ValidationError

from domain.models import IncomingTransaction
from utils.exceptions import (
    FailedToPublishMessageError,
    TransactionIntegrityError,
)


class ProcessingServiceStub:
    """Stub for the processing service."""

    def process_transaction(
        self,
        transaction: IncomingTransaction,
    ) -> dict[str, str]:
        """Process the transaction."""
        if transaction.transaction_id == "error_integrity":
            raise TransactionIntegrityError(transaction_id=1)
        if transaction.transaction_id == "error_publish":
            raise FailedToPublishMessageError
        if transaction.transaction_id == "validation_error":
            raise ValidationError
        return {"status": "success"}
