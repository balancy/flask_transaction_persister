"""Module for queue client."""

from __future__ import annotations

import json
import uuid
from typing import Any

import pika


class QueueClient:
    """Queue client class."""

    def __init__(
        self,
        queue_host: str = "transaction-rabbitmq",
        queue_name: str = "transaction-queue",
    ) -> None:
        """Initialize RabbitMQ connection."""
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=queue_host),
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

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
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                content_encoding="utf-8",
                content_type="application/json",
            ),
        )

    def close_connection(self) -> None:
        """Close RabbitMQ connection."""
        self.connection.close()
