"""Setting up database initialization."""

from flask import Flask

from config import DATABASE_URL
from infrastructure.persistence.extensions import db


def init_db(app: Flask) -> None:
    """Initialize database."""
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
