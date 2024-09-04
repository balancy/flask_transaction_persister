"""Main flask app."""

from flask import Flask
from flask_injector import FlaskInjector

from config import IS_TRACING_ON
from dependencies import configure_dependencies_for_app
from presentation.routes import routes_blueprint

if IS_TRACING_ON:
    from utils.tracing import (
        init_instruments_for_flask_app,
        initialize_tracing,
    )


def create_app() -> Flask:
    """Create the Flask app."""
    if IS_TRACING_ON:
        initialize_tracing(service_name="web-service + db")

    app = Flask(__name__)
    app.register_blueprint(routes_blueprint)

    if IS_TRACING_ON:
        init_instruments_for_flask_app(app)

    FlaskInjector(app=app, modules=[configure_dependencies_for_app])

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
