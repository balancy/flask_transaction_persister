"""Module with stubs for external exchange rates service."""

from __future__ import annotations

from utils.exceptions import FailedToFetchExchangeRateError

CURRENCIES_PAIR = ("USD", "EUR")
RATE = 1.25


class ExternalExchangeRatesClientStub:
    """A stub implementation of the ExchangeRatesClientProtocol."""

    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Stub implementation of get_rate."""
        if (from_currency, to_currency) == CURRENCIES_PAIR:
            return RATE
        raise FailedToFetchExchangeRateError
