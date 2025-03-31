from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stdout,
    format="<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | "
           "<level>{level: <8}</level> | "
           "<white>{name}</white>:<white>{function}</white>:<white>{line}</white> - "
           "<level>{message}</level>",
    level="DEBUG",
    colorize=True,
)
