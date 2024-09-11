"""Logger initialization module."""

import logging


def setup_logger() -> logging.Logger:
    """Set up logger."""
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


logger = setup_logger()
