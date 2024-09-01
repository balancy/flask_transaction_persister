"""Main flask app."""

from http import HTTPStatus

from flask import Flask, jsonify, request
from flask.wrappers import Response
from loggers.app_logger import logger
from pydantic import ValidationError
from schemas.transaction_schema import IncomingTransactionSchema
from services.transaction_service import transaction_service_dependency
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)


@app.route("/")
def index() -> tuple[Response, HTTPStatus]:
    """Index route."""
    return jsonify({"status": "Server is running"}), HTTPStatus.OK


@app.route("/transaction", methods=["POST"])
def post_transaction() -> tuple[Response, HTTPStatus]:
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

    transaction_service = transaction_service_dependency()

    try:
        result = transaction_service.save_transaction(transaction_data)
        logger.info(
            "Transaction saved successfully: %s",
            transaction_data.transaction_id,
        )
        return jsonify(result), HTTPStatus.CREATED
    except IntegrityError:
        logger.error("----------------------------------------")
        logger.error(
            "Transaction ID already exists: %s",
            transaction_data.transaction_id,
        )
        return (
            jsonify({"error": "Transaction ID already exists"}),
            HTTPStatus.CONFLICT,
        )
    except Exception as ex:
        logger.error("+++++++++++++++++++++++++++++++++++++++++")
        logger.error(str(ex))
        return jsonify({"error": str(ex)}), HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    app.run(debug=True)
