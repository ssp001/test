import logging
import sys


def _logger_method(file_handeler) -> logging.Logger:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # check handelers
    if logger.hasHandlers():
        return logger
    # File handelers and system handdlers cofiguration
    fh = logging.FileHandler(file_handeler)
    sh = logging.StreamHandler(sys.stdout)
    # add format style
    formatt = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # add formater
    fh.setFormatter(formatt)
    sh.setFormatter(formatt)
    # add handelers
    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger
