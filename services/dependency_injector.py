"""Dependency injector module."""

from persistence.db import get_db
from services.transaction_service import TransactionService


def get_transaction_service() -> TransactionService:
    """Get the transaction service."""
    db_session = next(get_db())
    return TransactionService(db=db_session)
