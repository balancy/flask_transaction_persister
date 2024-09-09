"""Module with tests for the domain layer models."""

from datetime import datetime

from domain.models import IncomingTransaction, ProcessedTransaction


def test_incoming_transaction_model_methods() -> None:
    """Test IncomingTransaction model methods."""
    correct_incoming_transaction = IncomingTransaction(
        transaction_id="123",
        user_id="456",
        amount=100,
        currency="USD",
        timestamp=datetime(2022, 1, 1),  # noqa: DTZ001
    )
    transaction_dict_form = correct_incoming_transaction.to_dict()
    assert (
        IncomingTransaction.from_dict(transaction_dict_form)
        == correct_incoming_transaction
    )


def test_processed_transaction_model_methods() -> None:
    """Test ProcessedTransaction model methods."""
    correct_processed_transaction = ProcessedTransaction(
        transaction_id="123",
        user_id="456",
        original_amount=100,
        original_currency="USD",
        converted_amount=80,
        target_currency="EUR",
        exchange_rate=0.8,
        timestamp=datetime(2022, 1, 1),  # noqa: DTZ001
    )
    transaction_dict_form = correct_processed_transaction.to_dict()
    assert (
        ProcessedTransaction.from_dict(transaction_dict_form)
        == correct_processed_transaction
    )
