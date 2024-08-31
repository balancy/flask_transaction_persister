"""Transaction service module."""

from persistence.models import TransactionModel
from persistence.repo import TransactionRepository, repo_dependency
from schemas.transaction_schema import TransactionSchema


class TransactionService:
    """Transaction service class."""

    def __init__(self, repo: TransactionRepository = repo_dependency()) -> None:
        """Initialize service."""
        self.repo = repo

    def save_transaction(self, transaction_data: TransactionSchema) -> dict[str, str]:
        """Save transaction."""

        new_transaction = TransactionModel(
            transaction_id=transaction_data.transaction_id,
            user_id=transaction_data.user_id,
            amount=float(transaction_data.amount),
            currency=transaction_data.currency,
            timestamp=transaction_data.timestamp,
        )

        try:
            self.repo.add_transaction(new_transaction)
            return {"status": "Transaction saved successfully"}
        except Exception:
            raise


def service_dependency() -> TransactionService:
    """Get transaction service instance."""
    return TransactionService()
