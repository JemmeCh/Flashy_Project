import logging
import logging.config
import pathlib
import json

def setup_logging():
    config_file = pathlib.Path('src/flashy/services/logger/logger_config.json')
    with open(config_file) as f:
        config = json.load(f)
    logging.config.dictConfig(config)

def get_logger():
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