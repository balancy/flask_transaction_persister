"""Project configuration."""

from environs import Env

env = Env()
env.read_env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    "postgresql+psycopg2://username:password@localhost:5432/yourdatabase",
)
