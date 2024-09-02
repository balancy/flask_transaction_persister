"""Main flask app."""

from flask import Flask
from flask_injector import FlaskInjector

from factories import configure_dependencies
from presentation.routes import routes_blueprint


def create_app() -> Flask:
    """Create the Flask app."""
    app = Flask(__name__)

    app.register_blueprint(routes_blueprint)

    FlaskInjector(app=app, modules=[configure_dependencies])

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
