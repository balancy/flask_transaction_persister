"""Repositories module."""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.models import IncomingTransaction, ProcessedTransaction
from infrastructure.persistence.db import session_dependency
from infrastructure.persistence.models import (
    IncomingTransactionModel,
    ProcessedTransactionModel,
)
from utils.exceptions import TransactionIntegrityError


class TransactionRepository:
    """Repository class for handling database operations."""

    def __init__(self, db: Session | None = None) -> None:
        """Initialize repository with the database session."""
        self.db = db or session_dependency()

    def _save(
        self,
        transaction_data: IncomingTransaction | ProcessedTransaction,
        model: type[IncomingTransactionModel | ProcessedTransactionModel],
    ) -> IncomingTransactionModel | ProcessedTransactionModel:
        """Save transaction to the database."""
        transaction = model(**transaction_data.to_dict())

        try:
            self.db.add(transaction)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            id_ = transaction_data.transaction_id
            message = f"Transaction with ID {id_} already exists."
            raise TransactionIntegrityError(message) from None
        except Exception:
            self.db.rollback()
            raise

        return transaction

    def save_incoming_transaction(
        self,
        transaction_data: IncomingTransaction,
    ) -> IncomingTransactionModel:
        """Save incoming transaction to the database."""
        return self._save(transaction_data, IncomingTransactionModel)

    def save_modified_transaction(
        self,
        transaction_data: ProcessedTransaction,
    ) -> ProcessedTransactionModel:
        """Save transaction to the database."""
        return self._save(transaction_data, ProcessedTransactionModel)
