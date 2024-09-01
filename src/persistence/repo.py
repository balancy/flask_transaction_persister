"""Repositories module."""

from persistence.db import session_dependency
from persistence.models import TransactionModel
from schemas.transaction_schema import EnrichedTransactionSchema
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class TransactionRepository:
    """Repository class for handling transaction-related database operations."""

    def __init__(self, db: Session = session_dependency()) -> None:
        """Initialize repository with the database session."""
        self.db = db

    def add_transaction(
        self,
        transaction_data: EnrichedTransactionSchema,
    ) -> TransactionModel:
        """Add a new transaction to the database."""
        new_transaction = TransactionModel(
            transaction_id=transaction_data.transaction_id,
            user_id=transaction_data.user_id,
            original_amount=transaction_data.original_amount,
            original_currency=transaction_data.original_currency,
            converted_amount=transaction_data.converted_amount,
            exchange_rate=transaction_data.exchange_rate,
            target_currency=transaction_data.target_currency,
            timestamp=transaction_data.timestamp,
        )

        try:
            self.db.add(new_transaction)
            self.db.commit()
            self.db.refresh(new_transaction)
            return new_transaction
        except IntegrityError:
            self.db.rollback()
            raise
        except Exception:
            self.db.rollback()
            raise


def repo_dependency() -> TransactionRepository:
    """Get transaction repository intance."""
    return TransactionRepository()
