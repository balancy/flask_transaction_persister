"""Module for queue client."""

from __future__ import annotations

from typing import Any

from infrastructure.messaging.celery_config import celery_app


class QueueClient:
    """Queue client class."""

    def send_transaction_to_queue(
        self,
        transaction_data: dict[str, Any],
    ) -> None:
        """Send transaction processing task to the Celery queue."""
        celery_app.send_task(
            "infrastructure.messaging.tasks.process_transaction",
            args=[transaction_data],
        )
