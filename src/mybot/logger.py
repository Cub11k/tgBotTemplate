import sys
import os
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
        os.makedirs(os.path.dirname(logger_config.file_path), exist_ok=True)
        file_handler = logging.FileHandler(logger_config.file_path)
        file_handler.setFormatter(logging.Formatter(logger_config.format))
        logger.addHandler(file_handler)

    return logger
