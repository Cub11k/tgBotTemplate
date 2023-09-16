import sys
import logging

from .config.models import LoggerConfig


def setup_logger(logger_config: LoggerConfig):
    logger = logging.getLogger(logger_config.name)
    logger.setLevel(logger_config.level)

    if logger_config.stream:
        stream_handler = logging.StreamHandler(sys.stdout if logger_config.stream == 'stdout' else sys.stderr)
        stream_handler.setFormatter(logging.Formatter(logger_config.format))
        logger.addHandler(stream_handler)

    if logger_config.file_path:
        file_handler = logging.FileHandler(logger_config.file_path)
        file_handler.setFormatter(logging.Formatter(logger_config.format))
        logger.addHandler(file_handler)

    return logger
