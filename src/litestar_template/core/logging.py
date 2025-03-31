import logging


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    logger = logging.getLogger(name)
    logger.propagate = False

    log_format = "%(asctime)s: %(name)s: %(levelname)s: %(message)s"

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))

    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(format))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
