import logging

def setup_logger(name="TELU_EDOM_BOT", level=logging.DEBUG):
    """Creates and configures a logger instance.

    This function sets up a logger with a specific name and logging level.
    It attaches a `StreamHandler` that outputs logs to the console, using
    a simple timestamped log format. If the logger already has handlers,
    it avoids adding duplicate ones.

    Args:
        name (str, optional): Name of the logger. Defaults to "TELU_EDOM_BOT".
        level (int or str, optional): Logging level (e.g., logging.DEBUG, logging.INFO).
            Defaults to logging.DEBUG.

    Returns:
        logging.Logger: Configured logger instance ready for use.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger