"""Main flask app."""

from typing import Literal

from flask import Flask, jsonify, request
from flask.wrappers import Response
from pydantic import ValidationError

from loggers.app_logger import logger
from services.dependency_injector import get_transaction_service
from validators.trasaction import IncomingTransaction

app = Flask(__name__)


@app.route("/")
def index() -> tuple[Response, Literal[400] | Literal[200]]:
    """Index route."""
    return jsonify({"status": "Server is running"}), 200


@app.route("/transaction", methods=["POST"])
def post_transaction() -> tuple[Response, Literal[400] | Literal[200] | Literal[500]]:
    """Post transaction data to the server."""

    try:
        transaction_data = IncomingTransaction.model_validate(request.get_json())
        logger.info(f"Transaction received: %s", transaction_data.model_dump())
    except ValidationError as error:
        logger.error("Validation error: %s", error.errors())
        return jsonify({"error": str(error)}), 400

    logger.info(
        "Transaction processed successfully: %s",
        transaction_data.transaction_id,
    )

    transaction_service = get_transaction_service()

    try:
        result = transaction_service.save_transaction(transaction_data)
        logger.info(
            "Transaction saved successfully: %s",
            transaction_data.transaction_id,
        )
        return jsonify(result), 200
    except Exception as ex:
        logger.error(str(ex))
        return jsonify({"error": "Failed to save transaction"}), 500


if __name__ == "__main__":
    app.run(debug=True)
