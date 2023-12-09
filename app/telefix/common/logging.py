import inspect
import logging
import sys
from typing import Union

from loguru import logger


LOGGING_FORMAT = (
    "[<green>{time:YYYY-MM-DD HH:mm:ss}</green>] "
    "[<level>{level}</level>] "
    "[<bold>{name}</bold> | {function}() | line {line}] "
    "<level>{message}</level>"
)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: Union[str, int]
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(log_level: str):
    """
    Configures and sets up the logging for the application.

    - Removes any existing logger configurations.
    - Sets color codes for various logging levels.
    - Adds stdout as a logger output with a specified format and log level.

    Attributes Utilized:
        log_level: The level of logging to capture (e.g., DEBUG, INFO).

    Note:
        This method relies on the logger from an external library, and uses its methods
        for configuring the logging behavior.
    """
    logger.remove()

    logger.level("DEBUG", color="<cyan>")
    logger.level("INFO", color="<blue>")
    logger.level("SUCCESS", color="<green>")
    logger.level("WARNING", color="<yellow>")
    logger.level("ERROR", color="<red>")
    logger.level("CRITICAL", color="<RED><bg #f8bbd0>")

    logger.level("SECURITY", no=50, color="<RED>")

    logger.add(
        sys.stdout,
        level=f"{log_level}",
        colorize=True,
        format=LOGGING_FORMAT,
    )
    logger.debug("Loguru setup done")
