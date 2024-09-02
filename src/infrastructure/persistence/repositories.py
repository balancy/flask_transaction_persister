"""Repositories module."""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.models import Transaction
from infrastructure.persistence.db import session_dependency
from infrastructure.persistence.models import TransactionModel
from utils.exceptions import TransactionIntegrityError


class TransactionRepository:
    """Repository class for handling database operations."""

    def __init__(self, db: Session | None = None) -> None:
        """Initialize repository with the database session."""
        self.db = db or session_dependency()

    def save(
        self,
        transaction_data: Transaction,
    ) -> TransactionModel:
        """Save transaction to the database."""
        transaction = TransactionModel(**transaction_data.asdict())

        try:
            self.db.add(transaction)
            self.db.commit()
            self.db.refresh(transaction)
        except IntegrityError:
            self.db.rollback()
            id_ = transaction_data.transaction_id
            message = f"Transaction with ID {id_} already exists."
            raise TransactionIntegrityError(message) from None
        except Exception:
            self.db.rollback()
            raise

        return transaction
