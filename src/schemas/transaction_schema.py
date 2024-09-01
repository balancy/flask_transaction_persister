"""Incoming transaction schema module."""

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class IncomingTransactionSchema(BaseModel):
    """Incoming transaction schema."""

    transaction_id: Annotated[str, StringConstraints(min_length=1)]
    user_id: Annotated[str, StringConstraints(min_length=1)]
    amount: Annotated[float, Field(gt=0)]
    currency: Annotated[str, StringConstraints(min_length=3, max_length=3)]
    timestamp: datetime


@dataclass(frozen=True, slots=True)
class EnrichedTransactionSchema:
    """Enriched transaction schema.

    Includes converted amount, exchange rate and target currency.
    """

    transaction_id: str
    user_id: str
    original_amount: float
    original_currency: str
    converted_amount: float
    target_currency: str
    exchange_rate: float
    timestamp: datetime

    def asdict(self) -> dict:
        """Return transaction data as dictionary."""
        return asdict(self)
