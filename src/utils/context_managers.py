"""Module for context managers."""

from contextlib import contextmanager
from typing import Any, Generator

from config import IS_TRACING_ON


@contextmanager
def conditional_trace_context(
    module_name: str,
    span_name: str,
) -> Generator[Any, Any, None]:
    """Start a tracing span if IS_TRACING_ON is True."""
    if IS_TRACING_ON:
        from opentelemetry import trace

        tracer = trace.get_tracer(module_name)
        with tracer.start_as_current_span(span_name) as span:
            yield span
    else:
        yield None
