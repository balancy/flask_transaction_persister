"""Test celery tasks."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Generator
from unittest.mock import patch

import pytest

from tasks import process_transaction
from tests.stubs import NoOpLogger
from utils.exceptions import (
    FailedToFetchExchangeRateError,
    TransactionIntegrityError,
)

from .stubs.for_celery_tasks import (
    ProcessingServiceStub,
    celery_injector_stub,
    conditional_trace_context_stub,
)


@pytest.fixture(autouse=True)
def patch_celery_dependencies() -> Generator[None, Any, None]:
    """Fixture to patch dependencies for Celery tasks."""
    with (
        patch("utils.app_logger.logger", NoOpLogger(name="test")),
        patch("dependencies.celery_injector", celery_injector_stub),
        patch(
            "utils.context_managers.conditional_trace_context",
            conditional_trace_context_stub,
        ),
        patch("tasks.transaction_service", ProcessingServiceStub()),
    ):
        yield


@pytest.mark.parametrize(
    ("transaction_data", "expected_result", "expected_status"),
    [
        # Success Case
        (
            {
                "transaction_id": "success",
                "amount": 100,
                "currency": "USD",
                "user_id": "1",
                "timestamp": "2021-01-01T00:00:00",
            },
            {"status": "Processed transaction: success"},
            HTTPStatus.OK,
        ),
        # Transaction Integrity Error Case
        (
            {
                "transaction_id": "error_integrity",
                "amount": 200,
                "currency": "USD",
                "user_id": "2",
                "timestamp": "2021-01-01T01:00:00",
            },
            {"error": str(TransactionIntegrityError("error_integrity"))},
            HTTPStatus.CONFLICT,
        ),
        # Failed to Fetch Exchange Rate Error Case
        (
            {
                "transaction_id": "error_fetch_rate",
                "amount": 300,
                "currency": "USD",
                "user_id": "3",
                "timestamp": "2021-01-01T02:00:00",
            },
            {"error": str(FailedToFetchExchangeRateError())},
            HTTPStatus.BAD_REQUEST,
        ),
        # Validation Error Case
        (
            {
                "transaction_id": "validation_error",
                "amount": 400,
                "currency": "USD",
                "user_id": "4",
            },
            {"error": "Validation error"},
            HTTPStatus.BAD_REQUEST,
        ),
    ],
)
def test_process_transaction(
    transaction_data: dict,
    expected_result: dict[str, str],
    expected_status: HTTPStatus,
) -> None:
    """Test process_transaction task with various scenarios."""
    result, status = process_transaction(transaction_data)

    assert (result, status) == (expected_result, expected_status)
