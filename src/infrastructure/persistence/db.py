"""Database session creation module."""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine),
)


def session_dependency() -> Session:
    """Get the database session."""
    return SessionLocal()  # pragma: no cover
