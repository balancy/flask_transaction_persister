from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, Any, None]:
    """Get the database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
