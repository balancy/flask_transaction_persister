"""Transaction service module."""

from sqlalchemy.orm.session import Session

from persistence.models import TransactionModel
from validators.trasaction import IncomingTransaction


class TransactionService:
    """Transaction service class."""

    def __init__(self, db: Session) -> None:
        """Initialize service."""
        self.db = db

    def save_transaction(self, transaction_data: IncomingTransaction) -> dict[str, str]:
        """Save transaction."""

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
            return {"status": "Transaction saved successfully"}
        except Exception as ex:
            self.db.rollback()
            raise Exception(f"Failed to save transaction: {ex}")
