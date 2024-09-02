"""Module for ExchangeRatesService class."""

from injector import inject

from config import TARGET_CURRENCY
from infrastructure.external_api.clients import ExternalExchangeRatesClient


class ExchangeRatesService:
    """Class for exchange rates service."""

    @inject
    def __init__(
        self,
        external_client: ExternalExchangeRatesClient,
    ) -> None:
        """Initialize service."""
        self.target_currency = TARGET_CURRENCY
        self.external_client = external_client

    def get_rate(self, incoming_currency: str) -> float:
        """Get exchange rate."""
        return self.external_client.get_rate(
            incoming_currency,
            self.target_currency,
        )
