"""Tests for repositories."""

from datetime import datetime
from typing import Any, Generator

import pytest
from psycopg2.extensions import connection
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from domain.models import IncomingTransaction, ProcessedTransaction
from infrastructure.persistence.models import Base
from infrastructure.persistence.repositories import TransactionRepository
from utils.exceptions import TransactionIntegrityError


@pytest.fixture()
def db_session(postgresql: connection) -> Generator[Session, Any, None]:
    """Fixture that sets up a database session for testing."""
    conn_info = postgresql.info
    db_url = (
        f"postgresql+psycopg2://{conn_info.user}:{conn_info.password}"
        f"@{conn_info.host}:{conn_info.port}/{conn_info.dbname}"
    )
    engine = create_engine(url=db_url)

    Base.metadata.create_all(engine)

    session_factory = scoped_session(sessionmaker(bind=engine))
    session = session_factory()

    yield session

    session.rollback()
    session.close()
    session_factory.remove()
    engine.dispose()


@pytest.fixture()
def transaction_repository(db_session: Session) -> TransactionRepository:
    """Fixture that provides a TransactionRepository."""
    return TransactionRepository(db=db_session)


@pytest.fixture()
def incoming_transaction() -> IncomingTransaction:
    """Fixture for IncomingTransaction."""
    return IncomingTransaction(
        transaction_id="123",
        amount=100.0,
        currency="USD",
        user_id="456",
        timestamp=datetime(2021, 1, 1),  # noqa: DTZ001
    )


@pytest.fixture()
def processed_transaction() -> ProcessedTransaction:
    """Fixture for ProcessedTransaction."""
    return ProcessedTransaction(
        transaction_id="123",
        original_amount=100.0,
        original_currency="USD",
        converted_amount=80.0,
        target_currency="EUR",
        exchange_rate=0.8,
        user_id="456",
        timestamp=datetime(2021, 1, 1),  # noqa: DTZ001
    )


def test_save_incoming_transaction_success(
    transaction_repository: TransactionRepository,
    incoming_transaction: IncomingTransaction,
) -> None:
    """Test saving an incoming transaction successfully."""
    result = transaction_repository.save_incoming_transaction(
        incoming_transaction,
    )

    for field in incoming_transaction.to_dict():
        assert getattr(result, field) == getattr(incoming_transaction, field)


def test_save_incoming_transaction_integrity_error(
    transaction_repository: TransactionRepository,
    incoming_transaction: IncomingTransaction,
) -> None:
    """Test saving an incoming transaction that raises an IntegrityError."""
    transaction_repository.save_incoming_transaction(incoming_transaction)

    with pytest.raises(TransactionIntegrityError):
        transaction_repository.save_incoming_transaction(incoming_transaction)


def test_save_processed_transaction_success(
    transaction_repository: TransactionRepository,
    processed_transaction: ProcessedTransaction,
) -> None:
    """Test saving a processed transaction successfully."""
    result = transaction_repository.save_processed_transaction(
        processed_transaction,
    )

    for field in processed_transaction.to_dict():
        assert getattr(result, field) == getattr(processed_transaction, field)


def test_save_processed_transaction_integrity_error(
    transaction_repository: TransactionRepository,
    processed_transaction: ProcessedTransaction,
) -> None:
    """Test saving a processed transaction that raises an IntegrityError."""
    transaction_repository.save_processed_transaction(processed_transaction)

    with pytest.raises(TransactionIntegrityError):
        transaction_repository.save_processed_transaction(
            processed_transaction,
        )
