"""Module for app routes."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from flask import Blueprint, Response, jsonify, request
from loggers.app_logger import logger
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src.schemas.transaction_schema import IncomingTransactionSchema

if TYPE_CHECKING:
    from services.transaction_service import TransactionService

blueprint = Blueprint("transaction", __name__)


@blueprint.route("/")
def index() -> tuple[Response, HTTPStatus]:
    """Index route."""
    return jsonify({"status": "Server is running"}), HTTPStatus.OK


@blueprint.route("/transaction", methods=["POST"])
def post_transaction(
    transaction_service: TransactionService,
) -> tuple[Response, HTTPStatus]:
    """Post transaction data to the server."""
    try:
        transaction_data = IncomingTransactionSchema.model_validate(
            request.get_json(),
        )
        logger.info("Transaction received: %s", transaction_data.model_dump())
    except ValidationError as error:
        logger.error("Validation error: %s", error.errors())
        return jsonify({"error": str(error)}), HTTPStatus.BAD_REQUEST

    logger.info(
        "Transaction processed successfully: %s",
        transaction_data.transaction_id,
    )

    try:
        result = transaction_service.save_transaction(transaction_data)
        logger.info(
            "Transaction saved successfully: %s",
            transaction_data.transaction_id,
        )
        return jsonify(result), HTTPStatus.CREATED
    except IntegrityError as ex:
        logger.error(str(ex))
        return (jsonify({"error": str(ex)}), HTTPStatus.CONFLICT)
