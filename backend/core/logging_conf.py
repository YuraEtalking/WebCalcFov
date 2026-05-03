import sys
from pathlib import Path

from loguru import logger


BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)


def setup_logger():
    """Установки логера."""
    logger.remove()

    logger.add(
        sys.stdout,
        level='DEBUG',
        colorize=True,
        format=(
            '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | '
            '<level>{level:<8}</level> | '
            '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - '
            '<level>{message}</level>'
        ),
    )

    logger.add(
        LOGS_DIR / 'app.log',
        level='ERROR',
        format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}',
        rotation='10 MB',
        retention='10 days',
        compression='zip',
        encoding='utf-8',
    )

    return logger