"""Fixtures for presentation layer tests."""

import logging

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_injector import FlaskInjector
from injector import Binder, singleton

from domain.protocols import ProcessingServiceProtocol
from presentation.routes import routes_blueprint
from tests.stubs import NoOpLogger

from .stubs import ProcessingServiceStub


def configure(binder: Binder) -> None:
    """Configure the presentation layer bindings."""
    binder.bind(
        ProcessingServiceProtocol,
        to=ProcessingServiceStub,
        scope=singleton,
    )
    binder.bind(logging.Logger, to=NoOpLogger("test"), scope=singleton)


@pytest.fixture
def app() -> Flask:
    """Create a Flask app."""
    app = Flask(__name__)
    app.register_blueprint(routes_blueprint)
    app.testing = True

    FlaskInjector(app=app, modules=[configure])

    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for the Flask app."""
    return app.test_client()
