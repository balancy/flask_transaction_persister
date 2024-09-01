"""Main flask app."""

from factories import configure_dependencies
from flask import Flask
from flask_injector import FlaskInjector
from routes import blueprint


def create_app() -> Flask:
    """Create the Flask app."""
    app = Flask(__name__)

    app.register_blueprint(blueprint)

    FlaskInjector(app=app, modules=[configure_dependencies])

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
