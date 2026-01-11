import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)s/%(funcName)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "etl.log",
            "formatter": "standard",
        },
    },

    "root": {
        "handlers": ["file"],
        "level": "INFO",
    },
}




def setup_logging(level=logging.INFO):
    dictConfig(LOGGING_CONFIG)

def get_logger(name:str):
    return logging.getLogger(name)