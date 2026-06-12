"""Observability setup: Prometheus metrics + Jaeger tracing."""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
from functools import wraps




def init_observability(service_name: str, jaeger_host: str = "localhost", jaeger_port: int = 6831):
    """Initialize Jaeger tracing and Prometheus metrics.

    Args:
        service_name: Name of the service for tracing
        jaeger_host: Jaeger agent host
        jaeger_port: Jaeger agent port
    """
    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": "1.0.0",
        }
    )

    jaeger_exporter = JaegerExporter(
        agent_host_name=jaeger_host,
        agent_port=jaeger_port,
    )

    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    trace.set_tracer_provider(trace_provider)


def metrics_endpoint(request) -> Response:
    """FastAPI route handler for Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


def traced(span_name: str = None):
    """Decorator to create a span for a function."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(span_name or func.__name__):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def get_tracer(name: str) -> trace.Tracer:
    """Get a tracer instance for manual span creation."""
    return trace.get_tracer(name)
