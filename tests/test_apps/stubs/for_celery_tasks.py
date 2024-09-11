"""Stubs for celery tasks."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator

from domain.models import IncomingTransaction
from utils.exceptions import (
    FailedToFetchExchangeRateError,
    TransactionIntegrityError,
)


@contextmanager
def conditional_trace_context_stub(
    _module_name: str,
    _span_name: str,
) -> Generator[Any, Any, None]:
    """Start a tracing span if IS_TRACING_ON is True."""
    yield None


class ProcessingServiceStub:
    """Stub for the processing service."""

    def process_transaction(
        self,
        transaction: IncomingTransaction,
    ) -> dict[str, str]:
        """Process the transaction."""
        transaction_id = transaction.transaction_id
        if transaction_id == "error_integrity":
            raise TransactionIntegrityError(transaction_id=transaction_id)

        if transaction_id == "error_fetch_rate":
            raise FailedToFetchExchangeRateError

        message = f"Processed transaction: {transaction_id}"

        return {"status": message}


class CeleryInjectorStub:
    """Stub for the celery injector."""

    def get(self, _protocol: type[object]) -> ProcessingServiceStub:
        """Get the processing service."""
        return ProcessingServiceStub()


celery_injector_stub = CeleryInjectorStub()
