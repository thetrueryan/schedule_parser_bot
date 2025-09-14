import logging
from logging import Logger
from logging.handlers import RotatingFileHandler

from src.core.settings import BASE_PATH

logger_path = BASE_PATH / "logs" / "app_logs.log"
logger_path.parent.mkdir(parents=True, exist_ok=True)


def setup_logger(lvl: int = logging.INFO) -> Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(level=lvl)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )

    file_handler = RotatingFileHandler(
        logger_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()
