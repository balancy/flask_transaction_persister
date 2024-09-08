"""Tests for exchange rates service logic."""

import pytest

from application.services.exchange_rates_service import ExchangeRatesService
from utils.exceptions import FailedToFetchExchangeRateError

from .stubs.for_exchange_rates_service import (
    CURRENCIES_PAIR,
    RATE,
    ExternalExchangeRatesClientStub,
)


@pytest.fixture
def exchange_rates_service() -> ExchangeRatesService:
    """Fixture for exchange rates service."""
    stub = ExternalExchangeRatesClientStub()
    return ExchangeRatesService(external_client=stub)


def test_get_rate_usd_to_eur(
    exchange_rates_service: ExchangeRatesService,
) -> None:
    """Test get_rate method for USD to EUR conversion using the stub."""
    rate = exchange_rates_service.get_rate(*CURRENCIES_PAIR)
    assert rate == RATE


def test_get_rate_failure(
    exchange_rates_service: ExchangeRatesService,
) -> None:
    """Test get_rate method when the rate is not found in the stub."""
    with pytest.raises(FailedToFetchExchangeRateError):
        exchange_rates_service.get_rate("GBP", "JPY")
