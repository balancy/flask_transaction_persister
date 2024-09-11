"""Tests for QueueClient class."""

from __future__ import annotations

import json
import uuid
from unittest.mock import Mock, patch

import pytest
from pika.exceptions import AMQPConnectionError

from infrastructure.messaging.queue_client import QueueClient
from utils.exceptions import FailedToPublishMessageError


@pytest.fixture
def queue_client() -> QueueClient:
    """Fixture for QueueClient."""
    return QueueClient()


@pytest.fixture
def mock_pika(mocker: Mock) -> tuple[Mock, Mock]:
    """Fixture for mocking pika library."""
    mock_connection = Mock()
    mock_channel = Mock()
    mock_connection.channel.return_value = mock_channel
    mocker.patch("pika.BlockingConnection", return_value=mock_connection)
    return mock_connection, mock_channel


def test_send_transaction_to_queue_passes_successfully(
    mock_pika: Mock,
    queue_client: QueueClient,
) -> None:
    """Test send_transaction_to_queue method."""
    _, mock_channel = mock_pika
    transaction_data = {"amount": 100, "currency": "USD"}
    expected_message = {
        "id": str(uuid.uuid4()),
        "task": "tasks.process_transaction",
        "args": [transaction_data],
        "kwargs": {},
        "retries": 0,
        "eta": None,
    }

    with patch("uuid.uuid4", return_value=uuid.UUID(expected_message["id"])):
        queue_client.send_transaction_to_queue(transaction_data)

    sent_message = json.loads(mock_channel.basic_publish.call_args[1]["body"])

    assert mock_channel.basic_publish.call_count == 1
    assert sent_message == expected_message


def test_send_transaction_to_queue_raises_error(
    mock_pika: Mock,
    queue_client: QueueClient,
) -> None:
    """Test send_transaction_to_queue method raises error on failure."""
    _, mock_channel = mock_pika
    transaction_data = {"amount": 100, "currency": "USD"}

    with patch.object(
        mock_channel,
        "basic_publish",
        side_effect=AMQPConnectionError,
    ), pytest.raises(FailedToPublishMessageError):
        queue_client.send_transaction_to_queue(transaction_data)


def test_close_connection(
    mock_pika: Mock,
    queue_client: QueueClient,
) -> None:
    """Test close_connection method."""
    _, _ = mock_pika

    queue_client.close_connection()

    assert queue_client.connection.is_closed
