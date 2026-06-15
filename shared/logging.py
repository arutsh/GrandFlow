import logging
import sys

import structlog
from structlog.types import Processor
from opentelemetry import trace


def _add_trace_id(_logger, _method_name, event_dict):
    span = trace.get_current_span()
    if span and span.is_recording():
        trace_id = span.get_span_context().trace_id
        event_dict["trace_id"] = f"{trace_id:032x}"
    return event_dict


def setup_logging(log_level: str = "INFO") -> None:
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors: list[Processor] = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        timestamper,
        _add_trace_id,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    structlog.configure(
        processors=shared_processors + [structlog.processors.JSONRenderer()],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        level=getattr(logging, (log_level or "INFO").upper(), logging.INFO),
        format="%(message)s",
        stream=sys.stdout,
    )

    logging.getLogger("pika").setLevel(logging.WARNING)


def get_logger(name: str) -> structlog.typing.FilteringBoundLogger:
    return structlog.get_logger(name)
