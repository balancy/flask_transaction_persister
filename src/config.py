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

BASE_CURRENCY = env.str("BASE_CURENCY", "EUR")
