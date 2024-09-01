"""Module for ExchangeRatesService class."""

import requests

from src.config import BASE_CURRENCY, EXCHANGE_RATES_API_URL

TIMEOUT = 5


class ExchangeRatesService:
    """Class for exchange rates service."""

    def __init__(
        self,
        exchange_rates_api: str = EXCHANGE_RATES_API_URL,
        base_currency: str = BASE_CURRENCY,
    ) -> None:
        """Initialize service."""
        self.exchange_rates_api = exchange_rates_api
        self.base_currency = base_currency

    def get_rate(self, currency: str) -> float:
        """Get exchange rate."""
        response = requests.get(
            f"{self.exchange_rates_api}{self.base_currency}",
            timeout=TIMEOUT,
        )
        response.raise_for_status()

        rates = response.json().get("rates", {})

        return rates.get(currency, 1.0)
