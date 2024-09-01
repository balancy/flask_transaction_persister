"""App database models."""

from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TransactionModel(Base):
    """Transaction model."""

    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    original_amount = Column(Float)
    original_currency = Column(String)
    converted_amount = Column(Float)
    target_currency = Column(String)
    exchange_rate = Column(Float)
    timestamp = Column(DateTime)
