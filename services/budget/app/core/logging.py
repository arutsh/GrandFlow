import logging
import sys
from typing import Any

import structlog
from pydantic_settings import BaseSettings


class LogConfig(BaseSettings):
    log_level: str = "INFO"

    class Config:
        env_file = ".env.budget.private.dev"
        case_sensitive = False


def setup_logging(log_level: str = "INFO") -> None:
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    structlog.configure(
        processors=shared_processors
        + [
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(message)s",
        stream=sys.stdout,
    )

    logging.getLogger("pika").setLevel(logging.WARNING)


def get_logger(name: str) -> structlog.typing.FilteringBoundLogger:
    return structlog.get_logger(name)
