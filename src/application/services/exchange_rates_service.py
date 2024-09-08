"""Module for ExchangeRatesService class."""

from injector import inject

from application.protocols import ExchangeRatesClientProtocol


class ExchangeRatesService:
    """Class for exchange rates service."""

    @inject
    def __init__(self, external_client: ExchangeRatesClientProtocol) -> None:
        """Initialize service."""
        self.external_client = external_client

    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Get exchange rate."""
        return self.external_client.get_rate(from_currency, to_currency)
