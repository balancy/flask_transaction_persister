"""Module containing tests for routes module."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask.testing import FlaskClient


ENDPOINT = "/transaction"


def test_post_transaction_with_success(client: FlaskClient) -> None:
    """Test post transaction finishes successfully."""
    transaction_data = {
        "transaction_id": "123",
        "amount": 100,
        "currency": "USD",
        "timestamp": "2023-01-01T00:00:00Z",
        "user_id": "123",
    }

    with client.application.app_context():
        response = client.post(ENDPOINT, json=transaction_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"status": "success"}


def test_post_transaction_with_validation_error(client: FlaskClient) -> None:
    """Test post transaction with validation error."""
    invalid_transaction_data = {
        "transaction_id": "123",
        "amount": 100,
        "currency": "USD",
        "timestamp": "2023-01-01T00:00:00Z",
    }

    with client.application.app_context():
        response = client.post(ENDPOINT, json=invalid_transaction_data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Validation failed" in response.json["error"]


def test_post_transaction_persisting_error(client: FlaskClient) -> None:
    """Test post transaction with persisting error."""
    transaction_data = {
        "transaction_id": "error_integrity",
        "amount": 100,
        "currency": "USD",
        "timestamp": "2023-01-01T00:00:00Z",
        "user_id": "123",
    }

    with client.application.app_context():
        response = client.post(ENDPOINT, json=transaction_data)

    assert response.status_code == HTTPStatus.CONFLICT
    assert "Transaction integrity error" in response.json["error"]


def test_post_transaction_with_failed_to_publish_error(
    client: FlaskClient,
) -> None:
    """Test post transaction with failed to publish to queue error."""
    transaction_data = {
        "transaction_id": "error_publish",
        "amount": 100,
        "currency": "USD",
        "timestamp": "2023-01-01T00:00:00Z",
        "user_id": "123",
    }

    with client.application.app_context():
        response = client.post(ENDPOINT, json=transaction_data)

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert "Failed to publish message" in response.json["error"]


def test_post_transaction_with_failed_to_fetch_rate_error(
    client: FlaskClient,
) -> None:
    """Test post transaction with failed to fetch rate error."""
    transaction_data = {
        "transaction_id": "error_fetch_rate",
        "amount": 100,
        "currency": "USD",
        "timestamp": "2023-01-01T00:00:00Z",
        "user_id": "123",
    }

    with client.application.app_context():
        response = client.post(ENDPOINT, json=transaction_data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Failed to fetch exchange rate" in response.json["error"]
