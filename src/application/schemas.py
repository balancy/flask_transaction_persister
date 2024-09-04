"""Validation schemas module."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class IncomingTransactionSchema(BaseModel):
    """Incoming transaction validation schema."""

    transaction_id: Annotated[str, StringConstraints(min_length=1)]
    user_id: Annotated[str, StringConstraints(min_length=1)]
    amount: Annotated[float, Field(gt=0)]
    currency: Annotated[str, StringConstraints(min_length=3, max_length=3)]
    timestamp: datetime
