"""Common stubs for all tests."""

from logging import Logger


class NoOpLogger(Logger):
    """A logger that does nothing."""

    def info(self, *args: str, **kwargs: str) -> None:
        """Do nothing."""

    def debug(self, *args: str, **kwargs: str) -> None:
        """Do nothing."""

    def error(self, *args: str, **kwargs: str) -> None:
        """Do nothing."""

    def warning(self, *args: str, **kwargs: str) -> None:
        """Do nothing."""

    def critical(self, *args: str, **kwargs: str) -> None:
        """Do nothing."""
