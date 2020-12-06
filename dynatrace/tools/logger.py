import logging
from os import makedirs
from os.path import exists
from dynatrace import settings

FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO, force_level=False):
    """ Setting up Loggers within the package

    Args:
        name (str): [description]
        log_file (str): [description]
        level (logging CONST, optional): Minimum Level to Log. Defaults to logging.INFO.

    Returns:
        FileHandler: New Logger to be used
    """
    #Initial Log Directory, if needed
    log_dir = settings.get_setting("LOG_DIR")
    if not exists(log_dir):
        makedirs(log_dir)

    if log_dir[-1] != '/':
        log_dir = log_dir + "/"
    handler = logging.FileHandler(f"{log_dir}{log_file}")
    handler.setFormatter(FORMATTER)

    logger = logging.getLogger(name)
    log_level = settings.get_setting("LOG_LEVEL")

    # Allowing the module to bypass user preferences and force it's own mode
    if log_level and not force_level:
        level = log_level
    if isinstance(level, str):
        level = getattr(logging, level)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger