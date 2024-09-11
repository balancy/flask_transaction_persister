"""Module for external api calls clients."""

import requests
from cachetools import TTLCache, cached

from config import EXCHANGE_RATES_API_URL
from utils.context_managers import conditional_trace_context
from utils.exceptions import FailedToFetchExchangeRateError

TIMEOUT = 5

cache = TTLCache(maxsize=100, ttl=60)


class ExternalExchangeRatesClient:
    """Handles communication with an external exchange rates API."""

    def __init__(self) -> None:
        """Initialize the client."""
        self.url = EXCHANGE_RATES_API_URL

    @cached(cache)
    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Fetch the conversion rate between two currencies."""
        try:
            with conditional_trace_context(__name__, "fetch_exchange_rate"):
                response = requests.get(
                    f"{self.url}/{from_currency}",
                    timeout=TIMEOUT,
                )
        except requests.RequestException:
            raise FailedToFetchExchangeRateError from None
        else:
            data = response.json()
            return data["rates"].get(to_currency, 1.0)
