"""Logger initialization module."""

import logging


def setup_logger() -> logging.Logger:
    """Set up logger."""
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("app.log")
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()
