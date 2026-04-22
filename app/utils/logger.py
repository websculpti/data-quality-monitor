import logging

from app.utils.config import LOG_LEVEL


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger.

    Ensures logging configuration is applied only once
    and avoids duplicate log handlers.
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        logging.basicConfig(
            level=LOG_LEVEL,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

    return logger