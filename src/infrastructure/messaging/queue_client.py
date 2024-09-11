"""Queue client module."""

from __future__ import annotations

import json
import uuid
from typing import Any

import pika
from pika.exceptions import AMQPConnectionError

from utils.context_managers import conditional_trace_context
from utils.exceptions import FailedToPublishMessageError


class QueueClient:
    """Queue client class."""

    def __init__(
        self,
        queue_host: str = "transaction-rabbitmq",
        queue_name: str = "transaction-queue",
    ) -> None:
        """Initialize RabbitMQ connection."""
        self._queue_name = queue_name
        self._queue_host = queue_host
        self._connection = None
        self._channel = None
        self._connect()

    def _connect(self) -> None:
        """Establish connection and channel to RabbitMQ."""
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._queue_host),
        )
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name, durable=True)

    def _reconnect_if_needed(self) -> None:
        """Reconnect to RabbitMQ if the channel is closed."""
        if self._channel is None or self._channel.is_closed:
            self._connect()

    def send_transaction_to_queue(
        self,
        transaction_data: dict[str, Any],
    ) -> None:
        """Send transaction data to the RabbitMQ queue."""
        message = {
            "id": str(uuid.uuid4()),
            "task": "tasks.process_transaction",
            "args": [transaction_data],
            "kwargs": {},
            "retries": 0,
            "eta": None,
        }

        try:
            with conditional_trace_context(__name__, "enqueue_transaction"):
                self._reconnect_if_needed()
                self._channel.basic_publish(
                    exchange="",
                    routing_key=self._queue_name,
                    body=json.dumps(message),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Make message persistent
                        content_encoding="utf-8",
                        content_type="application/json",
                    ),
                )
        except AMQPConnectionError:
            raise FailedToPublishMessageError from None

    def close_connection(self) -> None:
        """Close RabbitMQ connection."""
        if self._connection and not self._connection.is_closed:
            self._connection.close()
