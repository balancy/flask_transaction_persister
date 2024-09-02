"""Module for data transfer objects."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class TransactionDTO:
    """Data Transfer Object for carrying transaction data between layers."""

    transaction_id: str
    user_id: str
    amount: float
    currency: str
    timestamp: datetime
