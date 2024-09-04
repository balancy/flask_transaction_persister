"""Project configuration."""

from environs import Env

env = Env()
env.read_env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    "postgresql+psycopg2://username:password@localhost:5432/db",
)

EXCHANGE_RATES_API_URL = env.str(
    "EXCHANGE_RATES_API_URL",
    "https://api.exchangerate-api.com/v4/latest/",
)

TARGET_CURRENCY = env.str("TARGET_CURENCY", "EUR")

JAEGER_AGENT_HOST = env.str("JAEGER_AGENT_HOST", "transaction-jaeger")
JAEGER_AGENT_PORT = env.int("JAEGER_AGENT_PORT", 6831)

IS_TRACING_ON = env.str("FLASK_ENV", "development") == "development"

RABBITMQ_URL = env.str("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672//")
