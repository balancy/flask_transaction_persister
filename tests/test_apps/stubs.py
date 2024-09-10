"""Stubs for app tests."""

from __future__ import annotations

from typing import Callable, ClassVar, Literal

from flask import Blueprint, Flask, jsonify
from flask.wrappers import Response

routes_blueprint = Blueprint("routes_blueprint", __name__)


@routes_blueprint.route("/transaction", methods=["POST"])
def transaction_route() -> tuple[Response, Literal[200]]:
    """Stub method for transaction route."""
    return jsonify({"message": "Test response"}), 200


def initialize_tracing_for_flask_app(app: Flask, service_name: str) -> None:
    """Stub method to initialize tracing for a Flask app."""
    app.config["TRACING_INITIALIZED"] = True
    app.config["SERVICE_NAME"] = service_name


def configure_dependencies_for_web_app_stub() -> None:
    """Stub method to configure dependencies for a web app."""


class PrometheusMetricsStub:
    """Stub for PrometheusMetrics class."""

    apps: ClassVar[list[Flask]] = []

    def __init__(self, app: Flask) -> None:
        """Initialize the PrometheusMetricsStub."""
        self.app = app
        self.info_called = False
        self.name = None
        self.description = None
        self.labels = {}
        self.version = None

        PrometheusMetricsStub.apps.append(app)

    def info(self, name: str, description: str, version: str) -> None:
        """Stub method to simulate info method in Prometheus."""
        self.info_called = True
        self.name = name
        self.description = description
        self.version = version


class FlaskInjectorStub:
    """Stub for FlaskInjector class."""

    apps: ClassVar[list[Flask]] = []

    def __init__(self, app: Flask, modules: list[Callable]) -> None:
        """Initialize the FlaskInjectorStub."""
        self.app = app
        self.modules = modules

        FlaskInjectorStub.apps.append(app)
