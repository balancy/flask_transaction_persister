"""Module for testing custom context managers."""

from unittest.mock import patch

from utils.context_managers import conditional_trace_context

from .stubs import TraceStub


def test_conditional_trace_context_tracing_disabled() -> None:
    """Test conditional_trace_context when tracing is disabled."""
    with conditional_trace_context(
        "test_module",
        "test_span",
        is_tracing_on=False,
    ) as span:
        # When tracing is disabled, the context manager should yield None
        assert span is None


def test_conditional_trace_context_tracing_enabled() -> None:
    """Test conditional_trace_context when tracing is enabled."""
    with patch(
        "opentelemetry.trace",
        new=TraceStub(),
    ), conditional_trace_context(
        "test_module",
        "test_span",
        is_tracing_on=True,
    ) as span:
        assert span is not None
        assert span.name == "test_span"
