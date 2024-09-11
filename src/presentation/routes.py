"""Module for app routes."""

from __future__ import annotations

import logging  # noqa: TCH003
from http import HTTPStatus

from flask import Blueprint, Response, jsonify, request
from pydantic import ValidationError

from application.schemas import IncomingTransactionSchema
from domain.models import IncomingTransaction
from domain.protocols import ProcessingServiceProtocol
from utils.context_managers import conditional_trace_context
from utils.exceptions import (
    FailedToPublishMessageError,
    TransactionIntegrityError,
)

routes_blueprint = Blueprint("transaction", __name__)


@routes_blueprint.route("/transaction", methods=["POST"])
def post_transaction(
    transaction_service: ProcessingServiceProtocol,
    logger: logging.Logger,
) -> tuple[Response, HTTPStatus]:
    """Post transaction data to the server."""
    raw_data = request.get_json()
    logger.info("Data received: %s", raw_data)

    try:
        with conditional_trace_context(__name__, "validate_incoming_data"):
            validated_transaction = IncomingTransactionSchema.model_validate(
                raw_data,
            )
    except ValidationError as ex:
        logger.error("Validation error: %s", ex.errors())
        return (
            jsonify({"error": "Validation failed", "details": ex.errors()}),
            HTTPStatus.BAD_REQUEST,
        )

    logger.info(
        "Transaction validated: %s",
        validated_transaction.transaction_id,
    )

    transaction = IncomingTransaction(**validated_transaction.model_dump())

    try:
        with conditional_trace_context(__name__, "process_transaction"):
            result = transaction_service.process_transaction(transaction)
    except TransactionIntegrityError as ex:
        logger.error(ex.message)
        return (
            jsonify(
                {"error": "Transaction integrity error", "details": str(ex)},
            ),
            HTTPStatus.CONFLICT,
        )
    except FailedToPublishMessageError as ex:
        logger.error(str(ex.message))
        return (
            jsonify(
                {"error": "Failed to publish message", "details": str(ex)},
            ),
            HTTPStatus.SERVICE_UNAVAILABLE,
        )

    logger.info(result)
    return jsonify(result), HTTPStatus.CREATED
