"""
logger_setup.py
Configures application-wide logging to a file with timestamps.
Supports the Logging/Monitoring non-functional requirement.
"""

import logging
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")


def get_logger(name: str = "inventory_system") -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        # Avoid adding duplicate handlers if called multiple times
        return logger

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
