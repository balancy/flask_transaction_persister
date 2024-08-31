"""Repositories module."""

import psycopg2
from sqlalchemy.orm import Session

from persistence.db import session_dependency
from persistence.models import TransactionModel
from schemas.transaction_schema import TransactionSchema


class TransactionRepository:
    """Repository class for handling transaction-related database operations."""

    def __init__(self, db: Session = session_dependency()) -> None:
        """Initialize repository with the database session."""
        self.db = db

    def add_transaction(
        self,
        transaction_data: TransactionSchema,
    ) -> TransactionModel:
        """Add a new transaction to the database."""
        new_transaction = TransactionModel(
            transaction_id=transaction_data.transaction_id,
            user_id=transaction_data.user_id,
            amount=float(transaction_data.amount),
            currency=transaction_data.currency,
            timestamp=transaction_data.timestamp,
        )

        try:
            self.db.add(new_transaction)
            self.db.commit()
            self.db.refresh(new_transaction)
            return new_transaction
        except psycopg2.errors.UniqueViolation:
            self.db.rollback()
            raise Exception("Transaction ID already exists")
        except Exception as ex:
            self.db.rollback()
            raise Exception(f"Failed to save transaction: {ex}")


def repo_dependency() -> TransactionRepository:
    """Get transaction repository intance."""
    return TransactionRepository()
