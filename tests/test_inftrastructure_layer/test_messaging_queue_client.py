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


def test_send_transaction_to_queue_reconnects_if_channel_closed(
    mock_pika: Mock,
    queue_client: QueueClient,
) -> None:
    """Test send_transaction_to_queue reconnects if the channel is closed."""
    mock_connection, mock_channel = mock_pika
    mock_channel.is_closed = True

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

    mock_connection.channel.assert_called()
    sent_message = json.loads(mock_channel.basic_publish.call_args[1]["body"])

    assert mock_channel.basic_publish.call_count == 1
    assert sent_message == expected_message


def test_send_transaction_to_queue_passes_successfully(
    mock_pika: Mock,
    queue_client: QueueClient,
) -> None:
    """Test send_transaction_to_queue method under normal conditions."""
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


def test_send_transaction_to_queue_does_not_reconnect_if_channel_open(
    mock_pika: Mock,
    queue_client: QueueClient,
) -> None:
    """Test send transaction does not reconnect if the channel is open."""
    mock_connection, mock_channel = mock_pika
    mock_channel.is_closed = False

    transaction_data = {"amount": 100, "currency": "USD"}
    queue_client.send_transaction_to_queue(transaction_data)

    mock_connection.channel.assert_called_once()
    assert mock_channel.basic_publish.call_count == 1


def test_close_connection_closes_connection(
    mock_pika: Mock,
    queue_client: QueueClient,
) -> None:
    """Test close_connection method closes the connection if open."""
    mock_connection, _ = mock_pika
    mock_connection.is_closed = False

    queue_client.close_connection()

    mock_connection.close.assert_called_once()


def test_close_connection_does_nothing_if_already_closed(
    mock_pika: Mock,
    queue_client: QueueClient,
) -> None:
    """Test close_connection does nothing if connection is already closed."""
    mock_connection, _ = mock_pika
    mock_connection.is_closed = True

    queue_client.close_connection()

    mock_connection.close.assert_not_called()
