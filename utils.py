import logging
import sys


INFO = logging.INFO
DEBUG = logging.DEBUG
CRITICAL = logging.CRITICAL


def get_stream_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            style='{',
            fmt='[{asctime}] [{levelname}] {name}: {message}'
        )
    )
    logger.addHandler(handler)

    return logger