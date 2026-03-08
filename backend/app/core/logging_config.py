import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(log_level: str = "INFO") -> None:
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.set_name("uam-console")
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        logs_dir / "app.log",
        maxBytes=2 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.set_name("uam-file")
    file_handler.setFormatter(formatter)

    existing_names = {handler.get_name() for handler in logger.handlers}
    if "uam-console" not in existing_names:
        logger.addHandler(console_handler)
    if "uam-file" not in existing_names:
        logger.addHandler(file_handler)
