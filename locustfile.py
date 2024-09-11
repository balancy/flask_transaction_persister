"""Locust load test script for the API."""

import uuid

from locust import HttpUser, between, task


class TransactionUser(HttpUser):
    """Locust user classe."""

    wait_time = between(1, 3)

    @task
    def post_transaction(self) -> None:
        """Post a transaction to /transactio root."""
        transaction_id = str(uuid.uuid4())
        data = {
            "transaction_id": transaction_id,
            "amount": 100.0,
            "currency": "USD",
            "user_id": "123",
            "timestamp": "2024-09-11T00:00:00",
        }
        self.client.post("/transaction", json=data)
