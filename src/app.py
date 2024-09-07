"""Main flask app."""

from flask import Flask
from flask_injector import FlaskInjector

from config import IS_METRICS_MONITORING_ON, IS_TRACING_ON
from dependencies import configure_dependencies_for_web_app
from presentation.routes import routes_blueprint

if IS_METRICS_MONITORING_ON:
    from prometheus_flask_exporter import PrometheusMetrics


def create_app() -> Flask:
    """Create the Flask app."""
    app = Flask(__name__)
    app.register_blueprint(routes_blueprint)

    # tracing
    if IS_TRACING_ON:
        from utils.tracing import initialize_tracing_for_flask_app

        initialize_tracing_for_flask_app(app, "web-app")

    # monitoring metrics
    if IS_METRICS_MONITORING_ON:
        metrics = PrometheusMetrics(app)

        metrics.info("flask_app", "Transaction persister", version="0.1")

    # dependency injection
    FlaskInjector(app=app, modules=[configure_dependencies_for_web_app])

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
