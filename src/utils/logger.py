# src/utils/logger.py
import logging
import logging.handlers
import os
from pathlib import Path

LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"
ERROR_FILE = LOG_DIR / "error.log"

def get_logger(name: str = "medical_chatbot", level: int = logging.INFO):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(lineno)d | %(message)s"
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # Rotating file handler (INFO)
    fh = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # Error-specific rotating file handler (ERROR)
    eh = logging.handlers.RotatingFileHandler(
        ERROR_FILE, maxBytes=5 * 1024 * 1024, backupCount=7, encoding="utf-8"
    )
    eh.setLevel(logging.ERROR)
    eh.setFormatter(fmt)
    logger.addHandler(eh)

    logger.propagate = False
    return logger

logger = get_logger()
