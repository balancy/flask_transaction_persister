"""Create the database."""

from loggers.app_logger import logger
from persistence.db import engine
from persistence.models import Base


def init_db() -> None:
    """Initialize the database."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables are created successfully.")
    except Exception as e:
        logger.error("Failed to create tables: %s", str(e))


if __name__ == "__main__":
    init_db()
