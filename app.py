"""Main flask app."""

import logging
from typing import Literal

from flask import Flask, jsonify, request
from flask.wrappers import Response
from pydantic import ValidationError

from validation import IncomingTransaction

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)

app = Flask(__name__)


@app.route("/")
def index() -> tuple[Response, Literal[400] | Literal[200]]:
    """Index route."""
    return jsonify({"status": "Server is running"}), 200


@app.route("/transaction", methods=["POST"])
def post_transaction() -> tuple[Response, Literal[400] | Literal[200]]:
    """Post transaction data to the server."""

    try:
        transaction = IncomingTransaction.model_validate(request.get_json())
        logging.info(f"Transaction received: %s", transaction.model_dump())
    except ValidationError as error:
        logging.error("Validation error: %s", error.errors())
        return jsonify({"error": str(error)}), 400

    logging.info("Transaction processed successfully: %s", transaction.transaction_id)
    return jsonify({"status": "Transaction received successfully"}), 200
