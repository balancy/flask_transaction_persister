"""Module for ExchangeRatesService class."""

import requests

from src.config import BASE_CURRENCY, EXCHANGE_RATES_API_URL


class ExchangeRatesService:
    """Class for exchange rates service."""

    def __init__(
        self,
        exchange_rates_api: str = EXCHANGE_RATES_API_URL,
        base_currency: str = BASE_CURRENCY,
    ) -> None:
        self.exchange_rates_api = exchange_rates_api
        self.base_currency = base_currency

    def _get_rate_from_external_api(self, currency: str) -> float:
        """Make external API call."""
        response = requests.get(
            f"{self.exchange_rates_api}{self.base_currency}",
        )
        response.raise_for_status()

        rates = response.json().get("rates", {})
        return rates.get(currency, 1.0)

    def get_rate(self, currency: str) -> float:
        """Get exchange rate."""
        return self._get_rate_from_external_api(currency)


def get_exchange_rates_service() -> ExchangeRatesService:
    """Get exchange rates service instance."""
    return ExchangeRatesService()
