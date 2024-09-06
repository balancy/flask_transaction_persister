"""App database models."""

from infrastructure.persistence.extensions import db


class IncomingTransactionModel(db.Model):
    """Incoming transaction model."""

    __tablename__ = "incoming_transactions"

    transaction_id = db.Column(db.String, primary_key=True, index=True)
    user_id = db.Column(db.String, index=True)
    amount = db.Column(db.Float)
    currency = db.Column(db.String)
    timestamp = db.Column(db.DateTime)


class ProcessedTransactionModel(db.Model):
    """Processed transaction model."""

    __tablename__ = "transactions"

    transaction_id = db.Column(db.String, primary_key=True, index=True)
    user_id = db.Column(db.String, index=True)
    original_amount = db.Column(db.Float)
    original_currency = db.Column(db.String)
    converted_amount = db.Column(db.Float)
    target_currency = db.Column(db.String)
    exchange_rate = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
