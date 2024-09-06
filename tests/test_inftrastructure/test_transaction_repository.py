# """Tests for TransactionRepository class."""

# import datetime
# from typing import Any, Generator

# import pytest
# from sqlalchemy import Engine, create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm.session import Session
# from testcontainers.postgres import PostgresContainer

# from domain.models import IncomingTransaction, ProcessedTransaction
# from infrastructure.persistence.models import Base
# from infrastructure.persistence.repositories import TransactionRepository
# from utils.exceptions import TransactionIntegrityError


# @pytest.fixture(scope="session")
# def postgres_container() -> Generator[PostgresContainer, Any, None]:
#     """Create a new PostgreSQL container for testing."""
#     with PostgresContainer("postgres:16") as container:
#         container.start()
#         yield container


# @pytest.fixture(scope="session")
# def engine(postgres_container) -> Generator[Engine, Any, None]:
#     """Create a new database engine for testing."""
#     engine = create_engine(postgres_container.get_connection_url())

#     Base.metadata.create_all(engine)
#     yield engine

#     Base.metadata.drop_all(engine)


# @pytest.fixture(scope="function")
# def db_session(engine) -> Generator[Session, Any, None]:
#     """Provide a new session."""
#     connection = engine.connect()
#     transaction = connection.begin()
#     SessionLocal = sessionmaker(bind=engine)
#     session = SessionLocal(bind=connection)

#     yield session

#     transaction.rollback()
#     connection.close()
#     session.close()


# @pytest.fixture
# def transaction_repository(db_session) -> TransactionRepository:
#     """Provide a TransactionRepository with the test database session."""
#     return TransactionRepository(db=db_session)


# def test_save_incoming_transaction(transaction_repository) -> None:
#     """Test save_incoming_transaction method."""
#     incoming_transaction = IncomingTransaction(
#         transaction_id="tx123",
#         user_id="user123",
#         amount=100.0,
#         currency="USD",
#         timestamp=datetime.datetime(2024, 9, 5, 12, 0, 0),
#     )

#     saved_transaction = transaction_repository.save_incoming_transaction(
#         incoming_transaction,
#     )

#     for field in incoming_transaction.to_dict():
#         assert getattr(saved_transaction, field) == getattr(
#             incoming_transaction,
#             field,
#         )
