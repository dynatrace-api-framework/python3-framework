"""Module for logging throughout the framework."""
import logging
from logging import handlers
from dynatrace.framework import settings

logging.root.setLevel(logging.NOTSET)


def get_logger(name=__name__):
    """Sets up a logger and returns it for use throughout the framework.
    Actual configuration parameters are exposed in framework settings.
    \n
    @param name (str) - name of the logger. defaults to __name__
    \n
    @returns Logger - logger to be used in framework
    """
    enabled = settings.get_setting("LOG_ENABLED")
    output = settings.get_setting("LOG_OUTPUT")
    folder = settings.get_setting("LOG_DIR")
    level = settings.get_setting("LOG_LEVEL")
    logger = logging.getLogger(name)

    log_format = logging.Formatter(
        fmt="[%(asctime)s][%(module)s][%(funcName)s][%(levelname)s] %(message)s",
        datefmt="%Y-%b-%d %H:%M:%S"
    )

    if enabled:
        if "FILE" in output:
            file_handler = handlers.RotatingFileHandler(
                filename=f"{folder}/Framework.log",
                delay=True,
                maxBytes=1000000,
                backupCount=5
            )
            file_handler.setFormatter(log_format)
            file_handler.setLevel(level)
            logger.addHandler(file_handler)

        if "CONSOLE" in output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_format)
            console_handler.setLevel(level)
            logger.addHandler(console_handler)
    else:
        # Essentially disables logging
        logger.setLevel(logging.CRITICAL+1)

    return logger