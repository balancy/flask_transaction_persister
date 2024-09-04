"""Module for app routes."""

from __future__ import annotations

from http import HTTPStatus

from flask import Blueprint, Response, jsonify, request
from pydantic import ValidationError

from application.schemas import IncomingTransactionSchema
from application.services.processing_services import (
    IncomingTransactionProcessingService,
)
from domain.models import IncomingTransaction
from utils.app_logger import logger
from utils.exceptions import TransactionIntegrityError

routes_blueprint = Blueprint("transaction", __name__)


@routes_blueprint.route("/")
def index() -> tuple[Response, HTTPStatus]:
    """Index route."""
    return jsonify({"status": "Server is running"}), HTTPStatus.OK


@routes_blueprint.route("/transaction", methods=["POST"])
def post_transaction(
    transaction_service: IncomingTransactionProcessingService,
) -> tuple[Response, HTTPStatus]:
    """Post transaction data to the server."""
    raw_data = request.get_json()
    logger.info("Data received: %s", raw_data)

    try:
        transaction_data = IncomingTransactionSchema.model_validate(raw_data)
    except ValidationError as error:
        logger.error("Validation error: %s", error.errors())
        return jsonify({"error": str(error)}), HTTPStatus.BAD_REQUEST

    logger.info(
        "Transaction validated successfully: %s",
        transaction_data.transaction_id,
    )

    incoming_transaction = IncomingTransaction(**transaction_data.model_dump())

    try:
        result = transaction_service.process_transaction(incoming_transaction)
    except TransactionIntegrityError as ex:
        logger.error(str(ex))
        return jsonify({"error": str(ex)}), HTTPStatus.CONFLICT

    logger.info(result)
    return jsonify(result), HTTPStatus.CREATED
