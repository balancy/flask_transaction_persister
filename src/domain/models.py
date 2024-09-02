"""Domain models."""

from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Transaction:
    """Transaction domain model."""

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
