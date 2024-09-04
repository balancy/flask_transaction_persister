"""tracing module."""

from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.pika import PikaInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from config import JAEGER_AGENT_HOST, JAEGER_AGENT_PORT
from utils.app_logger import logger


def _initialize_tracing(service_name: str) -> None:
    """Initialize tracing."""
    resource = Resource(attributes={"service.name": service_name})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    exporter = JaegerExporter(
        agent_host_name=JAEGER_AGENT_HOST,
        agent_port=JAEGER_AGENT_PORT,
    )
    span_processor = BatchSpanProcessor(exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    Psycopg2Instrumentor().instrument(skip_dep_check=True)
    logger.info("Tracing initialized for the DB.")

    PikaInstrumentor().instrument()
    logger.info("Tracing initialized for the Rabbitmq.")


def initialize_tracing_for_flask_app(
    flask_app: Flask,
    service_name: str,
) -> None:
    """Initialize tracing for the Flask app."""
    _initialize_tracing(service_name)

    FlaskInstrumentor().instrument_app(flask_app)
    logger.info("Tracing initialized for Flask app.")


def initialize_tracing_for_celery_app(service_name: str) -> None:
    """Initialize tracing for the Celery app."""
    _initialize_tracing(service_name)

    CeleryInstrumentor()
    logger.info("Tracing initialized for Celery app.")
