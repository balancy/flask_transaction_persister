"""Domain models."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class ProcessedTransaction:
    """Processed transaction domain model."""

    transaction_id: str
    user_id: str
    original_amount: float
    original_currency: str
    converted_amount: float
    target_currency: str
    exchange_rate: float
    timestamp: datetime

    def to_dict(self) -> dict:
        """Return transaction data as dictionary."""
        return asdict(self)


@dataclass(frozen=True, slots=True)
class IncomingTransaction:
    """Incoming transactin domain model."""

    transaction_id: str
    user_id: str
    amount: float
    currency: str
    timestamp: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        data = asdict(self)
        data["timestamp"] = data["timestamp"].isoformat()
        return data

    @staticmethod
    def from_dict(data: dict) -> IncomingTransaction:
        """Create a IncomingTransaction from a dictionary."""
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return IncomingTransaction(**data)
