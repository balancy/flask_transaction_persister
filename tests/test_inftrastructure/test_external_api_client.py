"""Tests for ExternalApiClient class."""

from http import HTTPStatus

import pytest
import requests
import responses

from infrastructure.external_api_client import ExternalExchangeRatesClient


@pytest.fixture
def external_api_client() -> ExternalExchangeRatesClient:
    """Fixture for ExternalExchangeRatesClient."""
    return ExternalExchangeRatesClient()


@responses.activate
def test_get_rate_success(external_api_client) -> None:
    """Test get_rate method for successful response."""
    from_currency = "USD"
    to_currency = "EUR"
    expected_rate = 0.85

    responses.add(
        responses.GET,
        f"{external_api_client.url}/{from_currency}",
        json={"rates": {to_currency: expected_rate}},
        status=HTTPStatus.OK,
    )

    rate = external_api_client.get_rate(from_currency, to_currency)
    assert rate == expected_rate


@responses.activate
def test_get_rate_failure(external_api_client) -> None:
    """Test get_rate method for failed response."""
    from_currency = "USD"
    to_currency = "EUR"

    responses.add(
        responses.GET,
        f"{external_api_client.url}/{from_currency}",
        body=requests.RequestException("Network error"),
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(ConnectionError):
        external_api_client.get_rate(from_currency, to_currency)


@responses.activate
def test_get_rate_default(external_api_client) -> None:
    """Test get_rate method for default rate."""
    from_currency = "USD"
    to_currency = "NON_EXISTENT_CURRENCY"

    responses.add(
        responses.GET,
        f"{external_api_client.url}/{from_currency}",
        json={"rates": {}},
        status=HTTPStatus.OK,
    )

    rate = external_api_client.get_rate(from_currency, to_currency)
    assert rate == 1.0
