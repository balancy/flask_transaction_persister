"""Tests for repositories."""

from datetime import datetime
from typing import Any, Generator

import pytest
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from domain.models import IncomingTransaction, ProcessedTransaction
from infrastructure.persistence.models import Base
from infrastructure.persistence.repositories import TransactionRepository
from utils.exceptions import TransactionIntegrityError

TEST_DATABASE_URL = "postgresql+psycopg2://username:password@db:5432/test_db"


def create_test_database() -> None:
    """Create the test database if it does not exist."""
    host, db_name = TEST_DATABASE_URL.rsplit("/", 1)
    base_engine = create_engine(host + "/postgres", echo=False)

    with base_engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": db_name},
        ).scalar()

        if not result:
            conn.execute(text("CREATE DATABASE test_db"))
    base_engine.dispose()


@pytest.fixture(scope="session")
def engine() -> Generator[Engine, None, None]:
    """Set up the test database and ensure schema is created."""
    create_test_database()

    engine = create_engine(TEST_DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(
    engine: Engine,
) -> Generator[Session, Any, None]:
    """Fixture that sets up a database session for testing."""
    connection = engine.connect()
    session_factory = scoped_session(sessionmaker(bind=connection))
    session = session_factory()

    yield session

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(text(f"TRUNCATE TABLE {table.name};"))

    session.commit()
    session.close()
    session_factory.remove()
    engine.dispose()


@pytest.fixture
def transaction_repository(db_session: Session) -> TransactionRepository:
    """Fixture that provides a TransactionRepository."""
    return TransactionRepository(db=db_session)


@pytest.fixture
def incoming_transaction() -> IncomingTransaction:
    """Fixture for IncomingTransaction."""
    return IncomingTransaction(
        transaction_id="123",
        amount=100.0,
        currency="USD",
        user_id="456",
        timestamp=datetime(2021, 1, 1),  # noqa: DTZ001
    )


@pytest.fixture
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
