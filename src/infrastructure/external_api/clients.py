"""Module for external api calls clients."""

import requests

from config import EXCHANGE_RATES_API_URL

TIMEOUT = 5


class ExternalExchangeRatesClient:
    """Handles communication with an external exchange rates API."""

    def __init__(self) -> None:
        """Initialize the client."""
        self.url = EXCHANGE_RATES_API_URL

    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Fetch the conversion rate between two currencies."""
        try:
            response = requests.get(
                f"{self.url}/{from_currency}",
                timeout=TIMEOUT,
            )
        except requests.RequestException as e:
            message = f"Failed to fetch exchange rate: {e!s}"
            raise ConnectionError(message) from None
        else:
            data = response.json()
            return data["rates"].get(to_currency, 1.0)
