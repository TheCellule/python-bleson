from logging import basicConfig, getLogger, INFO, DEBUG, WARN, WARNING, ERROR

""" Simple convenience wrapper around Python's standard logging. """

LOGGER_NAME='bleson'
LOG_FORMAT= '%(asctime)s %(levelname)6s - %(filename)24s:%(lineno)3s - %(funcName)24s(): %(message)s'

basicConfig(level=INFO, format=LOG_FORMAT)
log = getLogger(LOGGER_NAME)

def set_level(level):
    """ Set the Bleson module logging level."""
    logger = getLogger(LOGGER_NAME)
    previous_level = logger.level
    logger.setLevel(level)
    return previous_level