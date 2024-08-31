"""Incoming transaction validation."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class IncomingTransaction(BaseModel):
    """Incoming transaction data."""

    transaction_id: Annotated[str, StringConstraints(min_length=1)]
    user_id: Annotated[str, StringConstraints(min_length=1)]
    amount: Annotated[float, Field(gt=0)]
    currency: Annotated[str, StringConstraints(min_length=3, max_length=3)]
    timestamp: datetime
