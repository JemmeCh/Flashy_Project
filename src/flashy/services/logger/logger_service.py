import logging
import logging.config
import pathlib
import json

def setup_logging():
    """
    Configure application-wide logging using a JSON configuration file.
    
    This function loads a logging configuration from
    ``src/flashy/services/logger/logger_config.json`` and applies it using
    :func:`logging.config.dictConfig`.
    
    The configuration defines loggers, handlers, formatters, and logging
    levels used throughout the application.
    
    :returns: None
    :rtype: None
    
    :raises FileNotFoundError: If the logging configuration file does not exist.
    :raises json.JSONDecodeError: If the configuration file contains invalid JSON.
    :raises ValueError: If the logging configuration is invalid.
    """
    config_file = pathlib.Path('src/flashy/services/logger/logger_config.json')
    with open(config_file) as f:
        config = json.load(f)
    logging.config.dictConfig(config)

def get_logger():
    """
    Retrieve the main application logger instance named ``"flashy"``,
    which is defined in the logging configuration loaded by
    :func:`setup_logging`.
    
    :returns: Configured application logger.
    :rtype: logging.Logger
    """
    return logging.getLogger("flashy")



def main():
    """:meta private:"""
    setup_logging()
    logger = logging.getLogger('flashy')
    
    logging.basicConfig(level="INFO")
    logger.debug("debug message", extra={"x": "hello"})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    try:
        1 / 0 #type:ignore
    except ZeroDivisionError:
        logger.exception("exception message")

if __name__ == "__main__":
    main()