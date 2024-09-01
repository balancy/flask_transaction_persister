"""Repositories module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from persistence.db import session_dependency
from persistence.models import TransactionModel
from sqlalchemy.exc import IntegrityError

if TYPE_CHECKING:
    from schemas.transaction_schema import EnrichedTransactionSchema
    from sqlalchemy.orm import Session


class TransactionRepository:
    """Repository class for handling database operations."""

    def __init__(self, db: Session | None = None) -> None:
        """Initialize repository with the database session."""
        self.db = db or session_dependency()

    def save(
        self,
        transaction_data: EnrichedTransactionSchema,
    ) -> TransactionModel:
        """Save transaction to the database."""
        transaction = TransactionModel(**transaction_data.asdict())

        try:
            self.db.add(transaction)
            self.db.commit()
            self.db.refresh(transaction)
        except IntegrityError:
            self.db.rollback()
            raise
        except Exception:
            self.db.rollback()
            raise

        return transaction
