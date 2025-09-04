import logging
import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure loguru logger
config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            "level": settings.LOG_LEVEL if hasattr(settings, "LOG_LEVEL") else "INFO",
        },
        {
            "sink": log_dir / "app.log",
            "rotation": "10 MB",
            "retention": "1 week",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            "level": settings.LOG_LEVEL if hasattr(settings, "LOG_LEVEL") else "INFO",
        },
    ],
}

# Configure loguru with the config
logger.configure(**config)


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages toward Loguru."""

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    """Configure standard library logging to use loguru."""
    # Intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.LOG_LEVEL if hasattr(settings, "LOG_LEVEL") else "INFO")

    # Remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Configure uvicorn logging
    logging.getLogger("uvicorn").handlers = []
    logging.getLogger("uvicorn.access").handlers = []
    logging.getLogger("uvicorn.error").handlers = []

    # Configure other third-party modules
    logging.getLogger("sqlalchemy").handlers = []
    logging.getLogger("sqlalchemy.engine").handlers = []

    logger.info("Logging system configured")