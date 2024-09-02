"""Module for data transfer objects."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class TransactionDTO:
    """Data Transfer Object for carrying transaction data between layers."""

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
    def from_dict(data: dict) -> TransactionDTO:
        """Create a TransactionDTO from a dictionary."""
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return TransactionDTO(**data)
