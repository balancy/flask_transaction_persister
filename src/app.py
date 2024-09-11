"""Main flask app."""

from flask import Flask
from flask_injector import FlaskInjector

from config import IS_METRICS_MONITORING_ON, IS_TRACING_ON
from dependencies import configure_dependencies_for_web_app
from presentation.routes import routes_blueprint

if IS_METRICS_MONITORING_ON:  # pragma: no cover
    from prometheus_flask_exporter import PrometheusMetrics


def create_app(
    is_metrics_on: bool = IS_METRICS_MONITORING_ON,  # noqa: FBT001
    is_tracing_on: bool = IS_TRACING_ON,  # noqa: FBT001
) -> Flask:
    """Create the Flask app."""
    app = Flask(__name__)
    app.register_blueprint(routes_blueprint)

    # tracing
    if is_tracing_on:
        from utils.tracing import initialize_tracing_for_flask_app

        initialize_tracing_for_flask_app(app, "web-app")

    # monitoring metrics
    if is_metrics_on:
        metrics = PrometheusMetrics(app)

        metrics.info("flask_app", "Transaction persister", version="0.1")

    # dependency injection
    FlaskInjector(app=app, modules=[configure_dependencies_for_web_app])

    return app
