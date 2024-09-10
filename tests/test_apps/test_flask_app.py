"""Test flask app creation."""

from http import HTTPStatus
from unittest.mock import patch

import pytest
from flask import Flask

from app import create_app

from .stubs import (
    FlaskInjectorStub,
    PrometheusMetricsStub,
    configure_dependencies_for_web_app_stub,
    initialize_tracing_for_flask_app,
    routes_blueprint,
)


@pytest.fixture(scope="module")
def test_app_with_flags_on() -> Flask:
    """Create Flask app with metrics and tracing ON."""
    tracing, metrics = True, True
    with (
        patch("app.IS_METRICS_MONITORING_ON", metrics),
        patch("app.IS_TRACING_ON", tracing),
        patch(
            "utils.tracing.initialize_tracing_for_flask_app",
            initialize_tracing_for_flask_app,
        ),
        patch("app.PrometheusMetrics", PrometheusMetricsStub),
        patch("app.FlaskInjector", FlaskInjectorStub),
        patch("app.routes_blueprint", routes_blueprint),
        patch(
            "dependencies.configure_dependencies_for_web_app",
            configure_dependencies_for_web_app_stub,
        ),
    ):
        app = create_app()
        app.config.update({"TESTING": True})
        return app


@pytest.fixture(scope="module")
def test_app_with_flags_off() -> Flask:
    """Create Flask app with metrics and tracing OFF."""
    tracing, metrics = False, False
    with (
        patch("app.IS_METRICS_MONITORING_ON", metrics),
        patch("app.IS_TRACING_ON", tracing),
        patch("app.FlaskInjector", FlaskInjectorStub),
        patch("app.routes_blueprint", routes_blueprint),
        patch(
            "dependencies.configure_dependencies_for_web_app",
            configure_dependencies_for_web_app_stub,
        ),
    ):
        app = create_app()
        app.config.update({"TESTING": True})
        return app


def test_app_creation(test_app_with_flags_on: Flask) -> None:
    """Test the creation of the Flask app."""
    assert isinstance(
        test_app_with_flags_on,
        Flask,
    ), "App should be an instance of Flask"
    assert (
        test_app_with_flags_on.config["TESTING"] is True
    ), "App should be in testing mode"


def test_blueprint_registration(test_app_with_flags_on: Flask) -> None:
    """Test that the routes blueprint is registered."""
    response = test_app_with_flags_on.test_client().post(
        "/transaction",
        json={},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"message": "Test response"}


def test_tracing_initialization_when_on(test_app_with_flags_on: Flask) -> None:
    """Test that tracing is on when True."""
    assert test_app_with_flags_on.config.get("TRACING_INITIALIZED")
    assert test_app_with_flags_on.config.get("SERVICE_NAME") == "web-app"


def test_no_tracing_initialization_when_off(
    test_app_with_flags_off: Flask,
) -> None:
    """Test that tracing is off when False."""
    assert not test_app_with_flags_off.config.get("TRACING_INITIALIZED")


def test_metrics_initialization_when_on(test_app_with_flags_on: Flask) -> None:
    """Test that Prometheus metrics are on when True."""
    assert test_app_with_flags_on in PrometheusMetricsStub.apps


def test_no_metrics_initialization_when_off(
    test_app_with_flags_off: Flask,
) -> None:
    """Test that Prometheus metrics are off when False."""
    assert test_app_with_flags_off not in PrometheusMetricsStub.apps


def test_dependency_injection(test_app_with_flags_on: Flask) -> None:
    """Test that FlaskInjector properly sets up dependencies."""
    assert test_app_with_flags_on in FlaskInjectorStub.apps
