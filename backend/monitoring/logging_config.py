import logging
import sys


def setup_logging(level=logging.INFO):
    """
    Global logging configuration for ChetnaOS.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger
