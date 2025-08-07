import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name='bot_logger', log_file='bot.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    # File handler (rotates)
    fh = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    fh.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.hasHandlers():
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

logger = setup_logger()
