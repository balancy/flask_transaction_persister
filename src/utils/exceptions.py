"""Module for exceptions."""

from __future__ import annotations


class TransactionIntegrityError(Exception):
    """Exception for transaction integrity errors."""

    def __init__(self, transaction_id: int | str, *args: str) -> None:
        """Initialize the exception."""
        message = f"Transaction with ID {transaction_id} already exists."
        super().__init__(message, *args)
        self.message = message

    def __str__(self) -> str:
        """Return the string representation of the exception."""
        return self.message


class FailedToPublishMessageError(Exception):
    """Exception for failed message publishing errors."""

    def __init__(self, *args: str) -> None:
        """Initialize the exception."""
        message = "Failed to publish message to queue."
        super().__init__(message, *args)
        self.message = message

    def __str__(self) -> str:
        """Return the string representation of the exception."""
        return self.message


class FailedToFetchExchangeRateError(Exception):
    """Exception for failed exchange rate fetching errors."""

    def __init__(self, *args: str) -> None:
        """Initialize the exception."""
        message = "Failed to fetch exchange rate."
        super().__init__(message, *args)
        self.message = message

    def __str__(self) -> str:
        """Return the string representation of the exception."""
        return self.message
